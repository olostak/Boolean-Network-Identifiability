import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)
import re

import unittest
from src import transition_graph as tg

# This is our test case for the add function
class UtilityFunctions(unittest.TestCase):

    def test_get_stable_values(self):
        timeseries= [
            ([0, 0],[0, 1]),
            ([0, 1],[1, 0]),
            ([1, 0],[1, 1]),
            ([1, 1],[1, 1]),
        ]

        expected = [
            ([0, 0], 0, 0),
            ([1, 0], 0, 1),
            ([1, 1], 0, 1),
            ([1, 1], 1, 1)
        ]
        self.assertEqual(tg.get_stable_values(timeseries), expected)

    def test_add_path_to_graph(self):
        graph = tg.TransitionGraph()
        state = [0, 0, 0]
        path = [1, 2, 0]
        tg.add_path_to_graph(graph, state, path)
        str_graph = graph.__str__()

        expected = "State: [0, 0, 0], Transitions: [1]\nState: [0, 1, 0], Transitions: [2]\nState: [0, 1, 1], Transitions: [0]\nState: [1, 1, 1], Transitions: []"
        self.assertEqual(str_graph, expected)

    def test_check_path_respect_stable_true(self):
        state = [0, 1]
        changes = [0, 1]
        stable = [
            ([0, 0], 0, 0),
            ([1, 0], 0, 1),
            ([1, 1], 0, 1),
        ]
        value = tg.check_path_respect_stable(changes, state, stable)
        self.assertTrue(value)

    def test_check_path_respect_stable_false(self):
        state = [0, 1]
        changes = [1, 0]
        stable = [
            ([0, 0], 0, 0),
            ([1, 0], 0, 1),
            ([1, 1], 0, 1),
        ]
        value = tg.check_path_respect_stable(changes, state, stable)
        self.assertFalse(value)

    def test_check_path_respect_stable_false2(self):
        state = [1, 0]
        changes = [0, 1]
        stable = [
            ([0, 0], 1, 0),
            ([1, 1], 1, 1),
            ([1, 1], 0, 1),
        ]
        value = tg.check_path_respect_stable(changes, state, stable)
        self.assertFalse(value)

    def test_get_truth_table(self):
        graph = tg.TransitionGraph()
        graph.add_transition([0, 0], [0, 1], 1)
        graph.add_transition([0, 1], [1, 1], 0)
        graph.add_transition([1, 1], [1, 0], 1)
        graph.add_transition([1, 0], [1, 1], 1)

        expected_truth_table = [
            ([0, 0], [0, 1]),
            ([0, 1], [1, 1]),
            ([1, 1], [1, 0]),
            ([1, 0], [1, 1])
        ]
        self.assertEqual(graph.get_truth_table(), expected_truth_table)


class ConstructTransitionGraph(unittest.TestCase):
    def test_transition_graph(self):
        timeseries= [
            ([0, 0],[0, 1]),
            ([0, 1],[1, 0]),
            ([1, 0],[1, 1]),
            ([1, 1],[1, 0]),
        ]

        graph = tg.transition_graph_construction(timeseries)
        expected_truth_table = [
                ([0, 0], [0, 1]),
                ([0, 1], [1, 1]),
                ([1, 1], [1, 0]),
                ([1, 0], [1, 1])
            ]
        self.assertEqual(graph.get_truth_table(), expected_truth_table)

    def test_non_existing_transision_graph(self):
        timeseries = [
            ([0, 0],[1, 0]),
            ([0, 1],[1, 0]),
            ([1, 0],[0, 1]),
            ([1, 1],[1, 1]),
        ]

        graph = tg.transition_graph_construction(timeseries)
        expected_truth_table = [([0, 0], [1, 0]), ([0, 1], [0, 0])]
        self.assertEqual(graph.get_truth_table(), expected_truth_table)

    def test_transition_graph_3vars(self):
        timeseries= [
            ([0, 0, 0],[0, 1, 0]),
            # ([0, 0, 1],[0, 1, 1]),
            # ([0, 1, 0],[0, 0, 0]),
            ([0, 1, 1],[1, 0, 1]),
            ([1, 0, 0],[0, 1, 0]),
            # ([1, 0, 1],[0, 1, 1]),
            # ([1, 1, 0],[0, 0, 0]),
            ([1, 1, 1],[1, 0, 1]),
        ]

        graph = tg.transition_graph_construction(timeseries)
        async_time_series = graph.get_async_time_series()
        print(async_time_series)

class ScipyApproximator(unittest.TestCase):
    def test_get_expression(self):
        def __replace_nonelementar_operations_expression(self, match):
            a, b = match.group(1), match.group(3)
            operation = match.group(2)

            if operation == 'xor':
                return f"({b} and not {a}) or ( not {b} and {a})"
            elif operation == 'nand':
                return f"not ({a} and {b})"
            elif operation == 'nor':
                return f"not ({a} or {b})"
            else:
                return match.group()
    
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
            pattern = r"(\d+) (xor|nand|nor) (\d+)"
            expression = re.sub(pattern, self.__replace_nonelementar_operations_expression, expression)
            return expression
        
        




# This is the entry point for running the tests
if __name__ == '__main__':
    unittest.main()