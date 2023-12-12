import os

MODEL = "cell_division"

output_path = f"./evaluate/{MODEL}/"
input_path = f"./evaluate/{MODEL}/time_series.txt"
psbn_path = f"./evaluate/{MODEL}/psbn_deterministic.aeon"
max_k = 9

os.system(f"python3 ./src/approximative_method.py --input_path {input_path} --psbn_path {psbn_path} --output_path {output_path} --max_k {max_k}")