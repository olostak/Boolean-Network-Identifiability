from itertools import permutations, product


class Node:
    def __init__(self, state):
        self.state = state
        self.transitions = {}

    def add_transition(self, to_node, label):
        self.transitions[label] = to_node

    def __str__(self):
        return f"State: {self.state}, Transitions: {list(self.transitions.keys())}"


class TransitionGraph:
    def __init__(self):
        self.nodes = {}

    def add_state(self, state):
        if str(state) not in self.nodes:
            self.nodes[str(state)] = Node(state)

    def add_transition(self, from_state, to_state, label):
        if str(from_state) not in self.nodes:
            self.add_state(from_state)
        if str(to_state) not in self.nodes:
            self.add_state(to_state)
        self.nodes[str(from_state)].add_transition(self.nodes[str(to_state)], label)

    def get_transitions(self, state):
        if str(state) in self.nodes:
            return self.nodes[str(state)].transitions
        else:
            return None

    def __str__(self):
        return '\n'.join(str(self.nodes[str(state)]) for state in self.nodes)

    def get_truth_table(self):
        truth_table = []
        for node_key in self.nodes:
            node = self.nodes[str(node_key)]
            if node.transitions.keys():
                state = node.state
                next_state = state.copy()
                for i in node.transitions.keys():
                    next_state[i] = (next_state[i] + 1 ) % 2
                truth_table.append((state, next_state))
        return truth_table
    
    def get_async_time_series(self):
        time_series = []
        for node_key in self.nodes:
            node = self.nodes[str(node_key)]
            if node.transitions.keys():
                state = node.state
                for i in node.transitions.keys():
                    next_state = state.copy()
                    next_state[i] = (next_state[i] + 1 ) % 2
                    time_series.append((state, next_state))
        return time_series



def check_path_respect_stable(changes, state, stable):
    prev_state = state.copy()
    for change in changes:
        for state, i, v in stable:
            if prev_state == state and change == i and (prev_state[change] + 1 ) % 2 != v:
                return False
        prev_state[change] = (prev_state[change] + 1 ) % 2
    return True

def add_path_to_graph(graph, state, path):
    prev_state = state
    for change in path:
        next_state = prev_state.copy()
        next_state[change] = (prev_state[change] + 1 ) % 2
        graph.add_transition(prev_state, next_state, change)
        prev_state = next_state

def get_stable_values(timeseries):
    stable = []
    for state, transition in timeseries:
        for i in range(len(state)):
            if state[i] == transition[i]:
                stable.append((state, i, transition[i]))
    return stable

def transition_graph_construction(timeseries):
    stable = get_stable_values(timeseries)
    graph = TransitionGraph()
    for state, transition in timeseries:
        changes = []
        for i in range(len(state)):
            if state[i] != transition[i]:
                changes.append(i)
        if len(changes) > 1:
            changes_permutation = permutations(changes)
            len_paths = 0
            for perm_changes in changes_permutation:
                if check_path_respect_stable(perm_changes, state, stable):
                    add_path_to_graph(graph, state, perm_changes)
                    len_paths += 1
            if len_paths == 0:
                return TransitionGraph()
        elif len(changes) == 1:
            # print(f"{state} -> {transition}")
            graph.add_transition(state, transition, changes[0])
    return graph

def truth_table_to_sop(truth_table):
    sop_functions = []
    for var_i in range(len(truth_table[0][0])):
        sop_terms = []
        for row in truth_table:
            inputs, output = row
            if output[var_i] == 1:
                term = []
                for idx, val in enumerate(inputs):
                    if val == 1:
                        term.append(f"x_{idx}")
                    else:
                        term.append(f"!x_{idx}")
                sop_terms.append(' & '.join(term))
        sop_functions.append(' | '.join(['({})'.format(item) for item in sop_terms]))
    return sop_functions   


def print_function(bn, compatible_instantiations):
    stg = SymbolicAsyncGraph(bn)
    projection = SymbolicProjection(stg, compatible_instantiations, retained_functions=["2"])
    for (state, functions) in projection:
        print([ function.to_string() for (var, function) in functions])


    

def generate_all_possible_functions(bn, n, timeserie, partial_bdd, state_variables):
    k = len(timeserie[0][0])
    all_combinations = list(product([1, 0], repeat=k))
    missing = len(all_combinations) - len(timeserie)
    missing_inputs = []
    for input_i in all_combinations:
        missing_flg = True
        for state in timeserie:
            if list(input_i) == state[0]:
                missing_flg = False
        if missing_flg:
            missing_inputs.append(input_i)
    missing_outputs = list(product([1, 0], repeat=missing))
    possible_functions = []
    counter = 0
    for i in range(len(missing_outputs)):
        truth_table = []
        for input, output in timeserie:
            truth_table.append((tuple(input), output[n]))
        for m in range(len(missing_outputs[i])):
            truth_table.append((tuple(missing_inputs[m]), missing_outputs[i][m]))
        expression = truth_table_to_sop(truth_table)

        update_function = UpdateFunction(expression, bn)
        bdd = ctx.mk_update_function_is_true(update_function)
        instantiations = partial_bdd.l_iff(bdd)
        instantiations = instantiations.project_for_all(state_variables)
        if not instantiations.is_false():
            print(">>>", expression)
            counter += 1
    print(f"{counter} / {len(missing_outputs)}")
    return possible_functions


def parse_partial_function(partial_function):
    partial_function_parts = partial_function.split(" ")
    

def add_path_to_list(list, state, path):
    prev_state = state
    p = [prev_state]
    for change in path:
        next_state = prev_state.copy()
        next_state[change] = (prev_state[change] + 1 ) % 2
        p.append(next_state)
        prev_state = next_state
    list.append(p)


def get_async_truth_tables(timeseries):
    stable = get_stable_values(timeseries)
    truth_tables = []
    paths = []
    essential_truth_table = {}
    for state, transition in timeseries:
        changes = []
        state_paths = []
        for i in range(len(state)):
            if state[i] != transition[i]:
                changes.append(i)
        if len(changes) > 1:
            changes_permutation = permutations(changes)
            len_paths = 0
            for perm_changes in changes_permutation:
                if check_path_respect_stable(perm_changes, state, stable):
                    add_path_to_list(state_paths, state, perm_changes)
                    len_paths += 1
            if len == 0:
                return []
            paths.append(state_paths)
        else:
            essential_truth_table[str(state)] = (state, transition)


    all_combinations = list(product(*paths))
    for combination in all_combinations:
        truth_table = essential_truth_table.copy()
        is_valid = True
        for p in combination:
            prev_state = p[0]
            for i in range(1, len(p)):
                if str(prev_state) not in truth_table.keys():
                    truth_table[str(prev_state)] = (prev_state, p[i])
                else:
                    if truth_table[str(prev_state)][1] != p[i]:
                        is_valid = False
                        break
                prev_state = p[i].copy()
            if not is_valid:
                print("is not valid")
                break
        if is_valid:
            truth_tables.append(list(truth_table.values()))

    return truth_tables
    """for tt in truth_tables:
        for row in tt.values():
            print(row)
        print("##############################################################")
    print(len(truth_tables))"""
    


"""timeseries = [
    ([0, 0, 0],[0, 1, 0]),
    ([0, 0, 1],[0, 1, 1]),
    ([0, 1, 0],[0, 0, 0]),
    ([0, 1, 1],[1, 0, 1]),
    ([1, 0, 0],[0, 1, 0]),
    ([1, 0, 1],[0, 1, 1]),
    ([1, 1, 0],[0, 0, 0]),
    ([1, 1, 1],[1, 0, 1]),
]

truth_tables = get_async_truth_tables(timeseries)
for truth_table in truth_tables:
    print(len(truth_table))
    for row in truth_table:
        print(row)"""





        

    
    