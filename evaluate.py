import os
import random

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

    """for i in range(len(time_series)):
        for j in range(len(time_series[0])):
            if random.random() < noise:
                time_series[i][j] = (time_series[i][j] + 1) % 2"""

    return boolean_network, time_series

random.seed(42)
input_paths = []
for i in range(len(timeseries) // 2):
    path = f"./evaluate/evaluate_missing_{i}.txt"
    input_paths.append(path)
    n = len(timeseries) - i  # Number of unique random numbers you want
    lines = random.sample(range(0, len(timeseries)), n)

    f = open(path, "w")
    for j in lines:
        f.write(f"{str(timeseries[j][0])},{str(timeseries[j][1])}\n")
    f.close()

for input_path in input_paths:
    output_path = input_path.replace(".txt", "")
    os.system(f"python3 ./aproximative_method.py --input_path {input_path} --output_path {output_path} --max_k 3")

for input_path in input_paths:
    output_path = input_path.replace(".txt", "")
    psbn_path = "test_psbn.aeon"
    os.system(f"python3 ./deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}")



"""expected_boolean_network, time_series  = generate_time_series(4, 5, 10, 0.4)
print(expected_boolean_network)
print(time_series)"""
