import os
from biodivine_aeon import *
from pathlib import Path
from benchmarks import *
import csv
import time


MODEL = "cell_division"
MODEL = "mir-9-neurogeneses"
#MODEL = "tumor_cell_invasion_and_migration"
input_path = f"./evaluate/{MODEL}/time_series.txt"
psbn_path = f"./evaluate/{MODEL}/psbn.aeon"

output_path = f"./evaluate/{MODEL}"

fieldnames = list(all_benchmarks.keys())
fieldnames.append("Running time")
with open(f"./evaluate/{MODEL}/banchmarks.csv", 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    original_string = Path(f"./evaluate/{MODEL}/original.aeon").read_text()
    bn_original = BooleanNetwork.from_aeon(original_string)

    for _ in range(30):
        start_time = time.time()
        os.system(f"python3 ./approximative_method.py --input_path {input_path} --psbn_path {psbn_path} --output_path {output_path} --max_k 25")
        end_time = time.time()


        infered_string = Path(f"{output_path}/infered.aeon").read_text()
        bn_infered = BooleanNetwork.from_aeon(infered_string)

        benchmarks_file = open(f"{output_path}/benchmarks.txt", "w")

        benchmarks_dict = {}
        for name, subpackage in all_benchmarks.items():
            value = subpackage.run_benchmark(bn_original, bn_infered)
            print(f"{name}: {value}")
            benchmarks_dict[name] = value
        benchmarks_dict["Running time"] = end_time - start_time
        writer.writerow(benchmarks_dict)


# psbn_path = "./test_timeseries/test_psbn.aeon"
# os.system(f"python3 ./deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}")



"""expected_boolean_network, time_series  = generate_time_series(4, 5, 10, 0.4)
print(expected_boolean_network)
print(time_series)"""


