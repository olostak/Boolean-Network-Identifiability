import re
import ast

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


def append_regulator(regulation_string, regulators):
    matches = re.search(r'->|-\||-\?', regulation_string)

    if matches:
        sign = matches.group()
        numbers = [int(s) for s in re.findall(r'\d+', regulation_string)]
        regulator = numbers[0]
        regulated = str(numbers[1])
        if regulated not in regulators.keys():
            regulators[regulated] = []
        if sign == "->":
            regulators[regulated].append(regulator)
        elif sign == "-|":
            regulators[regulated].append(-1 * regulator)
        else:
            regulators[regulated].append(regulator)
            regulators[regulated].append(-1 * regulator)

def read_regulators(path):
    regulators = {}
    try:
        with open(path, 'r') as file:
            for line in file:
                if line[0] != "$" and line[0] != "#":
                    append_regulator(line, regulators)
        return(regulators)
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