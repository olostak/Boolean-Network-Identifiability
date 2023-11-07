from biodivine_aeon import *
from itertools import combinations, product
import logicmin
import re

def truth_table_to_sop(truth_table):
    sop_terms = []

    for row in truth_table:
        inputs, output = row
        if output == 1:
            term = []
            for idx, val in enumerate(inputs):
                if val == 1:
                    term.append(f"x_{idx}")
                else:
                    term.append(f"!x_{idx}")
            sop_terms.append(' & '.join(term))
    return ' | '.join(['({})'.format(item) for item in sop_terms])


pattern = r'y\d+|not|\(|\)|<=|and|or|x\d+'
# Define a function to perform the substitutions
def replace(match):
    matched_text = match.group()
    if matched_text == "not":
        return "!"
    elif matched_text in {"(", ")", " "}:
        return ""
    elif matched_text == "or":
        return "|"
    elif matched_text == "and":
        return "&"
    elif matched_text.startswith("x"):
        return matched_text[1:]
    elif matched_text.startswith("y"):
        return ""
    


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
    #print(missing_inputs)
    #print(missing_outputs)
    possible_functions = []
    counter = 0
    for i in range(len(missing_outputs)):
        # version for sop boolean function
        truth_table = []
        for input, output in timeserie:
            truth_table.append((tuple(input), output[n]))
        for m in range(len(missing_outputs[i])):
            truth_table.append((tuple(missing_inputs[m]), missing_outputs[i][m]))
        #print(truth_table)
        expression = truth_table_to_sop(truth_table)
        #print(expression)

        # version for minimized boolean functions
        """for i in range(len(missing_outputs)):
        t = logicmin.TT(k,1)
        for input, output in timeserie:
            str_input = "".join(str(x) for x in input)
            t.add(str_input,(str)(output[n]))

        for m in range(len(missing_outputs[i])):
            str_missing_input = ''.join(str(x) for x in missing_inputs[m])
            t.add(str_missing_input,(str)(missing_outputs[i][m]))
        sols = t.solve()
        expression = sols.printN(xnames=[str(i) for i in range(k)], syntax='VHDL')
        expression = re.sub(pattern, replace, expression).lstrip()"""
        update_function = UpdateFunction(expression, bn)
        bdd = ctx.mk_update_function_is_true(update_function)
        instantiations = partial_bdd.l_iff(bdd)
        instantiations = instantiations.project_for_all(state_variables)
        if not instantiations.is_false():
            print(">>>", expression)
            counter += 1
            # print_function(bn, instantiations)
    print(f"{counter} / {len(missing_outputs)}")
    return possible_functions





rg = RegulatoryGraph(["x_0", "x_1", "x_2"])
rg.add_regulation({ 'source': "x_1", 'target': "x_0", 'observable': True })
rg.add_regulation({ 'source': "x_2", 'target': "x_0", 'observable': True })
rg.add_regulation({ 'source': "x_1", 'target': "x_1", 'observable': True })
rg.add_regulation({ 'source': "x_2", 'target': "x_2", 'observable': True })
bn = BooleanNetwork(rg)
bn.add_parameter({ 'name': "p1", 'arity': 2 })
bn.add_parameter({ 'name': "p2", 'arity': 1 })
bn.set_update_function("x_0", "p1(x_1, x_2)")
bn.set_update_function("x_1", "p2(x_1)")
bn.set_update_function("x_2", "x_2")

partial_functions = ["p1(x_1, x_2)", "p2(x_1)", "x_2"]

timeserie= [
([0, 0, 0],[0, 1, 0]),
# ([0, 0, 1],[0, 1, 1]),
# ([0, 1, 0],[0, 0, 0]),
([0, 1, 1],[1, 0, 1]),
([1, 0, 0],[0, 1, 0]),
# ([1, 0, 1],[0, 1, 1]),
# ([1, 1, 0],[0, 0, 0]),
([1, 1, 1],[1, 0, 1]),
]

stg = SymbolicAsyncGraph(bn)
ctx = SymbolicContext(bn)
bdd_ctx = ctx.bdd_variable_set()
network_variables = bn.variables()
state_variables = ctx.state_variables()
var_count = len(timeserie[0][0])

for var_i in range(var_count):
    print(">>> Variable", var_i)
    
    var_function = partial_functions[var_i]
    var_function = UpdateFunction(var_function, bn)
    partial_bdd = ctx.mk_update_function_is_true(var_function)

    # This BDD will represent all instantiations of the function in `partial_bdd` that 
    # agree with the time series observations. Initially, the set is unrestricted, 
    # and we gradually narrow it down as we add individual input-output pairs.
    valid_functions = bdd_ctx.mk_const(True)    
    for (source, target) in timeserie:
        assert len(source) == len(state_variables)
        assert len(target) == len(state_variables)

        # The output value expected for `var_function` assuming 
        # input corresponds to `source`.
        output = target[var_i]        

        # Convert the source vector to a list of `(symbolic_variable, bool_value)` pairs.
        source_valuation = list(zip(state_variables, [ bool(x) for x in source ]))        

        # Restrict `partial_bdd` to the source valuation. This basically leaves us
        # with a BDD which contains all instantiations of `partial_bdd` where 
        # the source input evaluates to true.
        partial_function_is_true = partial_bdd.select(source_valuation).project_exists(state_variables)
        # If the output is true, we just add this constraint to the result, otherwise
        # we add a negation of the constraint (i.e. BDD of instantiations where source
        # evaluates to false)
        if bool(output):
            valid_functions = valid_functions.l_and(partial_function_is_true)
        else:
            valid_functions = valid_functions.l_and_not(partial_function_is_true)
        
    # Now we can enumerate the satisfying valuations of the BDD.
    # This step relies on the fact that function of `var_i` in `bn` is exactly `partial_functions[var_i]`.    
    # In other words, if we want to use projection to inspect possible instantiations of a partial function,
    # said partial function has to be an update function for some of the network variables, because 
    # `SymbolicProjection` can only instantiate existing update functions from `bn`, not arbitrary ones.
    projection = SymbolicProjection(stg, valid_functions, retained_functions=[network_variables[var_i]])
    for (_var, fun) in projection:
        assert len(fun) == 1
        f = fun[0][1]
        print("\t", f.to_string(bn))


#for n in range(len(timeserie[0][0])):
#    print(f"Node {n}: {partial_functions[n]}")
#    partial = UpdateFunction(partial_functions[n], bn)
#    partial_bdd = ctx.mk_update_function_is_true(partial)
#    print(partial_bdd)
#    tree_functions = generate_all_possible_functions(bn, n, timeserie, partial_bdd, state_variables)



