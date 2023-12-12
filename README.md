# Boolean-Network-Identifiability

This repository contains implementation of two methods purposed for inferring Boolean networks from time-series data:

* <strong>Approximative method</strong>:

        ./src/approximative_method.py

* <strong>Deterministic method</strong>:

        ./src/deterministic_method.py

The scripts require at least Python 3.10 and specific packages listed in requirements.txt. To facilitate ease of use and ensure compatibility, a Docker image based on Ubuntu is provided, which comes pre-installed with all the necessary requirements.

1) install Docker [documentation](https://docs.docker.com/engine/install/)
2) build the docker image (it will take a few minutes):

        sudo docker build -t {image-name} .

3) run the docker image:

        sudo docker run -it {image-name}

4) display the content of directory:

        ls

We are now ready to execute one of the methods. The `./evaluate` directory contains three examples of models along with their corresponding synthetic data sets, demonstrating the usage and capabilities of these methods.

* cell_division
* mir-9-neurogeneses
* tumor_cell_invasion_and_migration

Examples of running the methods are in `./test_approximative.py` and `./test_deterministic.py`. We can run them with command:

* <strong>Approximative method</strong>:

        python3 test_deterministic.py

* <strong>Deterministic method</strong>:

        python3 test_approximative.py


Or we can run the scripts directly:

* <strong>Approximative method</strong>:

    The model directory can be easily changed in the script.

        ./src/approximative_method.py --input_path {input_path} --psbn_path {psbn_path} --output_path {output_path} --max_k {max_k}

* <strong>Deterministic method</strong>:

    It is recommended to apply this method primarily to the 'cell division' example, as it represents the smallest and most manageable dataset for demonstrating the efficacy of the technique.

        ./src/deterministic_method.py --ts_path {input_path} --psbn_path {psbn_path}

The final script, `evaluate_approximative.py`, executes the approximative method 30 times and assesses its performance using the benchmarks implemented in the `./benchmarks directory`. All the results are stored in the model directory.



