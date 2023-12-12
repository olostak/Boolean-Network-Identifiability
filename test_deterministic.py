import os


MODEL = "cell_division"

input_path = f"./evaluate/{MODEL}/time_series.txt"
psbn_path = f"./evaluate/{MODEL}/psbn_deterministic.aeon"
os.system(f"python3 ./src/deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}")