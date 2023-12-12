import random
import re

MODEL = "cell_division"

def read_functions_as_expressions(path):
    update_functions = []
    with open(path, 'r') as file:
        for line in file:
            if line[0] == '$':
                partial_function = line.split(":")[1].lstrip()
                update_functions.append(partial_function)
    expressions = []
    for update_function in update_functions:
        pattern = r'var_(\d+)'
        expression = update_function.replace('!', ' not ')
        expression = expression.replace('&', 'and')
        expression = expression.replace('|', 'or')
        expression = re.sub(pattern, r'int({\1})', expression)
        expressions.append(expression)
    return expressions

update_functions = read_functions_as_expressions(f"./evaluate/{MODEL}/original.aeon")

with open(f"./evaluate/{MODEL}/time_series.txt", 'w') as file:
    for _ in range(100):
        state = []
        time_series = []
        unique_tuples = set()
        for i in range(0, len(update_functions)):
            state.append(random.randint(0, 1))
        for _ in range(100):
            function_id = random.randint(0, (len(update_functions) - 1))
            next_state = state.copy()
            next_state[function_id] = int(eval(update_functions[function_id].format(*state)))
            if next_state != state:
                time_series.append((state, next_state))
                state = next_state
        i = 0
        while i < len(time_series):
            skip = random.randint(0, 3)
            if (i + skip) < len(time_series):
                state, _ = time_series[i]
                _, next_state = time_series[i + skip]
                unique_tuples.add(f"{state},{next_state}")
                i += skip
            else:
                state, next_state = time_series[i]
                unique_tuples.add(f"{state},{next_state}")
                i += 1

        for transition in unique_tuples:
            file.write(f"{transition}\n")