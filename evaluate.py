import os
import random
from biodivine_aeon import *
from pathlib import Path
from benchmarks import *
from helper_functions import read_time_serie


input_path = "./evaluate/cell_division_time_series1.txt"
psbn_path = "./evaluate/psbn.aeon"

output_path = "./evaluate/cell_division"
os.system(f"python3 ./approximative_method.py --input_path {input_path} --psbn_path {psbn_path} --output_path {output_path} --max_k 9")

infered_string = Path(f"{output_path}/infered.aeon").read_text()
bn_infered = BooleanNetwork.from_aeon(infered_string)

original_string = Path(f"./evaluate/original.aeon").read_text()
bn_original = BooleanNetwork.from_aeon(original_string)

benchmarks_file = open(f"{output_path}/benchmarks.txt", "w")

for name, subpackage in all_benchmarks.items():
    value = subpackage.run_benchmark(bn_original, bn_infered)
    print(f"{name}: {value}")
    benchmarks_file.write(f"{name}: {value}\n")

benchmarks_file.close()

# psbn_path = "./test_timeseries/test_psbn.aeon"
os.system(f"python3 ./deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}")



"""expected_boolean_network, time_series  = generate_time_series(4, 5, 10, 0.4)
print(expected_boolean_network)
print(time_series)"""


