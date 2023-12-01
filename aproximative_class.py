import sys
import sys
from biodivine_aeon import *
import re
from abc import ABC, abstractmethod
import os
from pathlib import Path
from wrapdisc.var import RandintVar
import graphviz

class BooleanNetworkApproximator(ABC):
    def __init__(self) -> None:
        self.LAMBDA = 10
        self.nodes = 0
        self.time_series = []
        self.node = 0
        self.k = 0

    def infer_boolean_network(self, time_series, known_regulators, max_K, output_path=None):
        boolean_network = []
        self.nodes = len(time_series[0][0])
        self.time_series = time_series
        errors = []
        for node in range(self.nodes):
            self.node = node
            min_uf = []
            min_fit = sys.maxsize
            for k in range(1, max_K):
                self.k = k
                bounds = self.__get_bounds()
                x0 = self.get_initial_solution(known_regulators[str(node)])
                solution = self.optimization(bounds, x0)
                fit = self.objective_function(solution)
                if fit < min_fit:
                    min_fit = fit
                    min_uf = list(solution)
            errors.append(min_fit)
            boolean_network.append(min_uf)

        if output_path:
            self.save_results(output_path, boolean_network, errors)
        return boolean_network, errors
    
    @abstractmethod
    def get_initial_solution(self, known_regulators):
        pass

    def __get_bounds(self):
        bounds = []
        for _ in range(self.k):
            bounds.append(RandintVar(-self.nodes, self.nodes-1))

        for _ in range(self.k-1):
            bounds.append(RandintVar(self.nodes*self.k, self.nodes*self.k + 1))
        return bounds

    @abstractmethod
    def objective_function(self, bf):
        pass
    
    @abstractmethod
    def optimization(self, bounds, x0):
        pass
    
    def __replace_nonelementar_operations(self, match):
        a, b = match.group(1), match.group(3)
        operation = match.group(2)

        if operation == 'xor':
            return f"({b} & !{a}) | (!{b} & {a})"
        elif operation == 'nand':
            return f"!({a} & {b})"
        elif operation == 'nor':
            return f"!({a} | {b})"
        else:
            return match.group()
            

    def __aeon_operations(self, x):
        y = x % self.nodes
        if y == 0:
            return "&"
        elif y == 1:
            return "|"
        elif y == 2:
            return "nor"
        elif y == 3:
            return "nand"
        elif y == 4:
            return "xor"

    def __get_aeon_format(self, node, bf):
        expression = f"$var_{node}: "
        n = round((len(bf) + 0.5) / 2)
        architecture = []
        for j in range(n):
            a = bf[j]
            edge = ""
            if a < 0:
                edge = f"var_{(a * -1) - 1} -| var_{node}\n"
                expression += "!" + f"var_{(a * -1) - 1} "
            else:
                edge = f"var_{a} -> var_{node}\n"
                expression += f"var_{a} "
            if (j + n) < len(bf):
                expression += f"{self.__aeon_operations(bf[j + n])} "
            architecture.append(edge)
        expression += "\n"
        return architecture, expression

    def create_aeon_file(self, bn, path):
        pattern = r"(\d+) (xor|nand|nor) (\d+)"
        f = open(path, "w")
        for i in range(len(bn)):
            arch, func = self.__get_aeon_format(i, bn[i])
            func = re.sub(pattern, self.__replace_nonelementar_operations, func)
            for edge in arch:
                f.write(edge)
            f.write(func)
        f.close()

    def display_graph(self, path, bn):
        dot = graphviz.Digraph("aproximated_bn")
        for node in range(self.nodes):
            dot.node(str(node), str(node))
        for i in range(len(bn)):
            bf = bn[i]
            for j in range(round((len(bf) + 0.5) / 2)):
                if bf[j] >= 0:
                    dot.edge(str(bf[j]), str(i))
                else:
                    dot.edge(str(abs(bf[j]) - 1), str(i), style="dashed")
        dot.render(filename=path)

    def save_results(self, path, bn, errors):
        if not os.path.exists(path):
            try:
                # Create the directory
                os.makedirs(path)
            except OSError as error:
                print(f"Creation of the directory '{path}' failed due to: {error}")
        self.create_aeon_file(bn, f"./{path}/infered.aeon")

        # display_graph("expected", expected_boolean_network, nodes)
        self.display_graph(f"./{path}/infered", bn)
        model_string = Path(f"./{path}/infered.aeon").read_text()
        errors_file = open(f"./{path}/errors.txt", "w")
        for i in range(len(errors)):
            errors_file.write(f"Node: {i} Error: {errors[i]}\n")
        errors_file.close()
        model = BooleanNetwork.from_aeon(model_string)
        print(model.to_aeon())    