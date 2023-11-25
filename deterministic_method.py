from biodivine_aeon import *
from asynchronose_boolaen_networks import *
import ast
import argparse

def read_time_serie(path):
    time_series = []
    try:
        with open(path, 'r') as file:
            for line in file:
                list_strs = line.split('],[', 1)
                if len(list_strs) == 2:
                    list1 = ast.literal_eval(list_strs[0] + ']')
                    list2 = ast.literal_eval('[' + list_strs[1])
                    time_series.append((list1, list2))
                else:
                    print("Invalid line format:", line.strip())
        return time_series
    except FileNotFoundError:
        print(f"The file {path} was not found.")
    except IOError:
        print(f"An error occurred while reading the file {path}.")

def read_partial_functions(path):
    partial_functions = []
    try:
        with open(path, 'r') as file:
            for line in file:
                if line[0] == '$':
                    partial_function = line.split(":")[1].lstrip()
                    partial_functions.append(partial_function)
        return partial_functions
    except FileNotFoundError:
        print(f"The file {path} was not found.")
    except IOError:
        print(f"An error occurred while reading the file {path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script with named parameters.")

    # Add arguments
    parser.add_argument("--ts_path", type=str, help="Time series file.")
    parser.add_argument("--psbn_path", type=str, help="PSBN file.")

    # Parse arguments
    args = parser.parse_args()

    timeseries_path = args.ts_path
    psbn_path = args.psbn_path

    timeseries = read_time_serie(timeseries_path)
    partial_functions = read_partial_functions(psbn_path)

    """transition_graph = transition_graph_construction(timeseries)
    non_complete_truth_table = transition_graph.get_truth_table()"""
    async_truth_tables = get_async_truth_tables(timeseries)
    if async_truth_tables:
        bn = BooleanNetwork.from_file(psbn_path)

        stg = SymbolicAsyncGraph(bn)
        ctx = SymbolicContext(bn)
        bdd_ctx = ctx.bdd_variable_set()
        network_variables = bn.variables()
        state_variables = ctx.state_variables()
        var_count = len(async_truth_tables[0][0][0])
        for non_complete_truth_table in async_truth_tables:
            # print(non_complete_truth_table)
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

            print("############################################################")


"""
>>> Variable 0
         (x_1 & x_2)
>>> Variable 1
         (((!x_0 & !x_1) | ((!x_0 & x_1) & x_2)) | ((x_0 & x_1) & !x_2))
>>> Variable 2
         x_2
############################################################
>>> Variable 0
         (((!x_0 & x_1) & x_2) | (x_0 & x_1))
>>> Variable 1
         ((!x_0 & !x_1) | ((!x_0 & x_1) & x_2))
>>> Variable 2
         x_2
############################################################
>>> Variable 0
         ((((!x_0 & x_1) & x_2) | ((x_0 & !x_1) & !x_2)) | ((x_0 & x_1) & x_2))
>>> Variable 1
         (((!x_0 & !x_1) | ((!x_0 & x_1) & x_2)) | (x_0 & !x_2))
>>> Variable 2
         x_2
"""
