import os

input_path = "./test_timeseries/timeseries3.txt"
psbn_path = "./test_timeseries/test_psbn.aeon"

os.system(f"python3 ./deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}")