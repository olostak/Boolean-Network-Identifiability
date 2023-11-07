from itertools import permutations 


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
            state = node.state
            next_state = state.copy()
            for i in node.transitions.keys():
                next_state[i] = (next_state[i] + 1 ) % 2
            truth_table.append((str(state), str(next_state)))
        return truth_table

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
            graph.add_transition(state, transition, changes[0])
    return graph


    