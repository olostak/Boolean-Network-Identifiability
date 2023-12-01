from aproximative_class import BooleanNetworkApproximator
from helper_functions import read_time_serie, read_regulators
import scipy.optimize
import random
from biodivine_aeon import *
from asynchronose_boolaen_networks import *
import argparse
# requirement python 3.10
from wrapdisc import Objective

class ScipyApproximator(BooleanNetworkApproximator):
    def __init__(self) -> None:
        super().__init__()

    def get_initial_solution(self, known_regulators):
        initial_solution = []
        for _ in range(self.k):
            r = random.randint(0, len(known_regulators) - 1)
            initial_solution.append(known_regulators[r])

        for _ in range(self.k-1):
            initial_solution.append(random.randint(self.nodes*self.k, self.nodes*self.k + 1))
        return initial_solution
    
    def optimization(self, bounds, x0):
        wrapped_objective = Objective(
                    self.objective_function,
                    variables=bounds
                )
        bounds = wrapped_objective.bounds

        ###############################################
        #        HERE IT IS POSSIBLE TO CHANGE        #
        #          THE OPTIMIZATION FUNCTION          #
        # #############################################

        result = scipy.optimize.minimize(wrapped_objective, x0, bounds=bounds)
        # result = scipy.optimize.differential_evolution(wrapped_objective, bounds=bounds)

        encoded_solution = result.x
        decoded_solution = list(wrapped_objective.decode(encoded_solution))
        return decoded_solution
    
    def __get_num_of_regulators(self, bf):
        return round((len(bf) + 0.5) / 2)
    
    def __operations(self, x):
        y = x % self.nodes
        if y == 0:
            return "and"
        elif y == 1:
            return "or"
        elif y == 2:
            return "nor"
        elif y == 3:
            return "nand"
        elif y == 4:
            return "xor"
    
    def __get_expression(self, bf):
        expression = ""
        n = round((len(bf) + 0.5) / 2)
        for j in range(n):
            a = bf[j]
            if a < 0:
                expression += "int(not {" + str((a * -1) - 1) + "}) "
            else:
                expression += "{" + str(a) + "} "
            if (j + n) < len(bf):
                expression += f"{self.__operations(bf[j + n])} "
        return expression
    
    def objective_function(self, bf):
        regulators = []
        # penalize solutions with repeting regulator
        for i in range(self.__get_num_of_regulators(bf)):
            if (bf[i] >= 0 and bf[i] in regulators) or (bf[i] < 0 and abs(bf[i] + 1) in regulators):
                return len(self.time_series)
            regulators.append(bf[i] if bf[i] >= 0 else abs(bf[i]) - 1)
        boolean_function = self.__get_expression(bf)
        error = 0
        for i in range(0, len(self.time_series)-1):
            target_val = eval(boolean_function.format(*self.time_series[i][0]))
            error += (self.time_series[i][1][self.node] - target_val)**2

        error = error + ((self.LAMBDA / (2 * len(self.time_series))) * round((len(bf) + 0.5) / 2))#regularization
        return error


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script with named parameters.")

    # Add arguments
    parser.add_argument("--input_path", type=str, help="Time series file.")
    parser.add_argument("--psbn_path", type=str, help="PSBN file path.")
    parser.add_argument("--output_path", type=str, help="Output directory.")
    parser.add_argument("--max_k", type=int, help="Maximum in degree.")

    # Parse arguments
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    time_series = read_time_serie(input_path)
    regulators = read_regulators(args.psbn_path)


    nodes = len(time_series[0][0])
    max_K = args.max_k
    transition_graph = transition_graph_construction(time_series)
    async_time_series = transition_graph.get_async_time_series()
    aproximator = ScipyApproximator()
    bn, errors = aproximator.infer_boolean_network(async_time_series, regulators, max_K, output_path)
