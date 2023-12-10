import os


MODEL = "cell_division"
#MODEL = "mir-9-neurogeneses"
input_path = f"./evaluate/{MODEL}/time_series.txt"
psbn_path = f"./evaluate/{MODEL}/psbn.aeon"
os.system(f"python3 ./deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}")