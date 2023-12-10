import random

update_functions = [
    "((((not {0} and {1}) and {2}) and not {3}) or (({0} and not {2}) and not {3}))",
    "(not {0} and {4})",
    "(({0} and not {2}) and not {3})",
    "({0} and not {4})",
    "((({0} and not {1}) and not {4}) and {3})"                                        
]

with open('cell_division_time_series3.txt', 'w') as file:
    for _ in range(5000):
        state = []
        time_series = []
        unique_tuples = set()
        for i in range(0, 5):
            state.append(random.randint(0, 1))
        for _ in range(1000):
            function_id = random.randint(0, 4)
            next_state = state.copy()
            next_state[function_id] = int(eval(update_functions[function_id].format(*state)))
            if next_state != state:
                time_series.append((state, next_state))
                #file.write(f"{state},{next_state}\n")
                #print(f"{state},{next_state}")
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