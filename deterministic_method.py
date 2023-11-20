from biodivine_aeon import *
from asynchronose_boolaen_networks import *

rg = RegulatoryGraph(["x_0", "x_1", "x_2"])
rg.add_regulation({ 'source': "x_0", 'target': "x_0", 'observable': True })
rg.add_regulation({ 'source': "x_1", 'target': "x_0", 'observable': True })
rg.add_regulation({ 'source': "x_2", 'target': "x_0", 'observable': True })
rg.add_regulation({ 'source': "x_1", 'target': "x_1", 'observable': True })
rg.add_regulation({ 'source': "x_2", 'target': "x_1", 'observable': True })
rg.add_regulation({ 'source': "x_0", 'target': "x_1", 'observable': True })
rg.add_regulation({ 'source': "x_2", 'target': "x_2", 'observable': True })
bn = BooleanNetwork(rg)
bn.add_parameter({ 'name': "p1", 'arity': 3 })
bn.add_parameter({ 'name': "p2", 'arity': 3 })
bn.set_update_function("x_0", "p1(x_0, x_1, x_2)")
bn.set_update_function("x_1", "p2(x_1, x_0, x_2)")
bn.set_update_function("x_2", "x_2")

partial_functions = ["p1(x_0, x_1, x_2)", "p2(x_1, x_0, x_2)", "x_2"]

timeseries= [
([0, 0, 0],[0, 1, 0]),
([0, 0, 1],[0, 1, 1]),
([0, 1, 0],[0, 0, 0]),
([0, 1, 1],[1, 0, 1]),
([1, 0, 0],[0, 1, 0]),
([1, 0, 1],[0, 1, 1]),
([1, 1, 0],[0, 0, 0]),
([1, 1, 1],[1, 0, 1]),
]

transition_graph = transition_graph_construction(timeseries)
non_complete_truth_table = transition_graph.get_truth_table()

stg = SymbolicAsyncGraph(bn)
ctx = SymbolicContext(bn)
bdd_ctx = ctx.bdd_variable_set()
network_variables = bn.variables()
state_variables = ctx.state_variables()
var_count = len(non_complete_truth_table[0][0])

for var_i in range(var_count):
    print(">>> Variable", var_i)
    
    var_function = partial_functions[var_i]
    var_function = UpdateFunction(var_function, bn)
    partial_bdd = ctx.mk_update_function_is_true(var_function)

    # This BDD will represent all instantiations of the function in `partial_bdd` that 
    # agree with the time series observations. Initially, the set is unrestricted, 
    # and we gradually narrow it down as we add individual input-output pairs.
    valid_functions = bdd_ctx.mk_const(True)    
    for (source, target) in non_complete_truth_table:
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
        functions = f.to_string(bn)
        print("\t", f.to_string(bn))
