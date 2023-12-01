import os

input_path = "./test_timeseries/timeseries3.txt"
output_path = "./test_aproximative_output"
psbn_path = "./test_timeseries/test_psbn.aeon"

os.system(f"python3 ./aproximative_method.py --input_path {input_path} --psbn_path {psbn_path} --output_path {output_path} --max_k 9")