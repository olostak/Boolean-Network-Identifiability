import scipy.optimize
import sys
import graphviz
from biodivine_aeon import *
from pathlib import Path
import random
import re
from asynchronose_boolaen_networks import *
import argparse
import ast
import os

# requirement python 3.10
from wrapdisc.var import RandintVar
from wrapdisc import Objective

LAMBDA = 0.5 # regularization parameter

pattern = r"(\d+) (xor|nand|nor) (\d+)"
def replace_nonelementar_operations(match):
    a, b = match.group(1), match.group(3)
    operation = match.group(2)

    if operation == 'xor':
        return f"({b} & !{a}) | (!{b} & {a})"
    elif operation == 'nand':
        return f"!({a} & {b})"
    elif operation == 'nor':
        return f"!({a} | {b})"
    else:
        return match.group()
    
def initial_vector(partial_function, nodes, k):
    partial_function_parts = partial_function.split(" ")
    in_named_function = False
    initial_vector = []
    for i in range(k):
        initial_solution.append(random.randint(-nodes, nodes-1))
        variables.append(RandintVar(-nodes, nodes-1))

    for i in range(k-1):
        initial_solution.append(random.randint(nodes*k, nodes*k + 1))
        variables.append(RandintVar(nodes*k, nodes*k + 1))
    print(variables)
    print(initial_solution)
    return variables, initial_solution
            

def aeon_operations(x, nodes):
        y = x % nodes
        if y == 0:
            return "&"
        elif y == 1:
            return "|"
        elif y == 2:
            return "nor"
        elif y == 3:
            return "nand"
        elif y == 4:
            return "xor"

def get_aeon_format(node, bf, nodes):
    expression = f"$var_{node}: "
    n = round((len(bf) + 0.5) / 2)
    architecture = []
    for j in range(n):
        a = bf[j]
        edge = ""
        if a < 0:
            edge = f"var_{(a * -1) - 1} -| var_{node}\n"
            expression += "!" + f"var_{(a * -1) - 1} "
        else:
            edge = f"var_{a} -> var_{node}\n"
            expression += f"var_{a} "
        if (j + n) < len(bf):
            expression += f"{aeon_operations(bf[j + n], nodes)} "
        architecture.append(edge)
    expression += "\n"
    return architecture, expression

def create_aeon_file(bn, path, nodes):
    f = open(path, "w")
    for i in range(len(bn)):
        arch, func = get_aeon_format(i, bn[i], nodes)
        func = re.sub(pattern, replace_nonelementar_operations, func)
        for edge in arch:
            f.write(edge)
        f.write(func)
    f.close()

def get_num_of_regulators(bf):
    return round((len(bf) + 0.5) / 2)


# Inputs:
#       * max_K maximum indegree
#       * time_serie - async time serie (matrix)
# Outputs:
#       * set of boolean functions
def infer_boolean_network(time_series, partial_functions, max_K):
    boolean_network = []
    nodes = len(time_series[0][0])

    def operations(x, nodes):
        y = x % nodes
        if y == 0:
            return "and"
        elif y == 1:
            return "or"
        elif y == 2:
            return "nor"
        elif y == 3:
            return "nand"
        elif y == 4:
            return "xor"

    def get_expression(bf):
        expression = ""
        n = round((len(bf) + 0.5) / 2)
        for j in range(n):
            a = bf[j]
            if a < 0:
                expression += "int(not {" + str((a * -1) - 1) + "}) "
            else:
                expression += "{" + str(a) + "} "
            if (j + n) < len(bf):
                expression += f"{operations(bf[j + n], nodes)} "
        return expression

    def get_bounds(k, partial_functions, nodes):
        variables = []
        initial_solution = []
        for i in range(k):
            initial_solution.append(random.randint(-nodes, nodes-1))
            variables.append(RandintVar(-nodes, nodes-1))

        for i in range(k-1):
            initial_solution.append(random.randint(nodes*k, nodes*k + 1))
            variables.append(RandintVar(nodes*k, nodes*k + 1))
        print(variables)
        print(initial_solution)
        return variables, initial_solution

    def objective_function(bf):

        regulators = []
        # penalize solutions with repeting regulator
        """for i in range(get_num_of_regulators(bf)):
            if (bf[i] >= 0 and bf[i] in regulators) or (bf[i] < 0 and abs(bf[i] + 1) in regulators):
                return len(time_series)
            regulators.append(bf[i] if bf[i] >= 0 else abs(bf[i]) - 1)"""
        boolean_function = get_expression(bf)
        error = 0
        for i in range(0, len(time_series)-1, 2):
            target_val = eval(boolean_function.format(*time_series[i][0]))
            error += (time_series[i][1][node] - target_val)**2
        error += (LAMBDA / (2 * len(time_series))) * round((len(bf) + 0.5) / 2) #regularization
        return error

    for node in range(nodes):
        min_uf = []
        min_fit = sys.maxsize
        for k in range(1, max_K):
            variables, x0 = get_bounds(k, partial_functions, nodes)
            wrapped_objective = Objective(
                objective_function,
                variables=variables
            )
            bounds = wrapped_objective.bounds

            ###############################################
            #        HERE IT IS POSSIBLE TO CHANGE        #
            #          THE OPTIMIZATION FUNCTION          #
            # #############################################

            # result = scipy.optimize.minimize(wrapped_objective, x0, bounds=bounds)
            result = scipy.optimize.differential_evolution(wrapped_objective, bounds=bounds)

            encoded_solution = result.x
            decoded_solution = list(wrapped_objective.decode(encoded_solution))
            fit = objective_function(decoded_solution)
            if fit < min_fit:
                min_fit = fit
                min_uf = list(decoded_solution)
        print(f"Node: {node} Error: {min_fit}")
        boolean_network.append(min_uf)

    return boolean_network


def generate_operations(x, nodes):
    y = x % nodes
    if y == 0:
        return "and"
    elif y == 1:
        return "or"

def generate_expression(bf, nodes):
    expression = ""
    n = round((len(bf) + 0.5) / 2)
    for j in range(n):
        a = bf[j]
        if a < 0:
            expression += "int(not {" + str((a * -1) - 1) + "}) "
        else:
            expression += "{" + str(a) + "} "
        if (j + n) < len(bf):
            expression += f"{generate_operations(bf[j + n], nodes)} "
    return expression

def generate_time_series(nodes, max_K, num_of_samples, noise):
    boolean_network = []
    for _ in range(nodes):
        update_function = []
        k = random.randint(1, max_K)
        counter = 0
        regulators = []
        while counter != k:
            regulator = random.randint(-nodes, nodes-1)
            if (regulator >= 0 and regulator not in regulators):
                update_function.append(regulator)
                regulators.append(regulator)
                counter += 1
            elif (regulator < 0 and abs(regulator + 1) not in regulators):
                update_function.append(regulator)
                regulators.append(abs(regulator) - 1)
                counter += 1

        for _ in range(k-1):
            update_function.append(random.randint(nodes*k, nodes*k + 1))
        boolean_network.append(update_function)

    time_series = []
    for _ in range(int(num_of_samples / 2)):
        time_point = []
        for _ in range(nodes):
            time_point.append(random.randint(0,1))
        time_series.append(time_point)
        next_timepoint = []
        for func in boolean_network:
            boolean_function = generate_expression(func, nodes)
            next_timepoint.append(eval(boolean_function.format(*time_point)))
        time_series.append(next_timepoint)

    for i in range(len(time_series)):
        for j in range(len(time_series[0])):
            if random.random() < noise:
                time_series[i][j] = (time_series[i][j] + 1) % 2

    return boolean_network, time_series

def display_graph(path, bn, nodes):
    dot = graphviz.Digraph("aproximated_bn")
    for node in range(nodes):
        dot.node(str(node), str(node))
    for i in range(len(bn)):
        bf = bn[i]
        for j in range(round((len(bf) + 0.5) / 2)):
            if bf[j] >= 0:
                dot.edge(str(bf[j]), str(i))
            else:
                dot.edge(str(abs(bf[j]) - 1), str(i), style="dashed")
    dot.render(filename=path)


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

def save_results(path, bn, nodes):
    if not os.path.exists(path):
        try:
            # Create the directory
            os.makedirs(path)
        except OSError as error:
            print(f"Creation of the directory '{path}' failed due to: {error}")
    create_aeon_file(bn, f"./{path}/infered.aeon", nodes)

    # display_graph("expected", expected_boolean_network, nodes)
    display_graph(f"./{path}/infered", bn, nodes)
    model_string = Path(f"./{path}/infered.aeon").read_text()
    # print(model_string)
    model = BooleanNetwork.from_aeon(model_string)
    print(model.to_aeon())

    


#################################################
# expected_boolean_network, time_series = generate_time_series(nodes, max_K, 30, 0.1)
"""print("Result:")
expected_string = Path('expected.aeon').read_text()
expected = BooleanNetwork.from_aeon(expected_string)
print(expected.to_aeon())"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script with named parameters.")

    # Add arguments
    parser.add_argument("--input_path", type=str, help="Time series file.")
    parser.add_argument("--output_path", type=str, help="Output directory.")
    parser.add_argument("--max_k", type=int, help="Maximum in degree.")

    # Parse arguments
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    time_series = read_time_serie(input_path)


    nodes = len(time_series[0][0])
    max_K = args.max_k
    transition_graph = transition_graph_construction(time_series)
    async_time_series = transition_graph.get_async_time_series()
    partial_functions = ["p1(x_2)", "p2(x_1, x_0, x_2)", "x_2"]
    bn = infer_boolean_network(async_time_series, partial_functions, max_K)
    save_results(output_path, bn, nodes)
    



