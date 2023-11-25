import os

input_path = "./timeseries3.txt"
output_path = "./test_aproximative_output"

os.system(f"python3 ./aproximative_method.py --input_path {input_path} --output_path {output_path} --max_k 9")