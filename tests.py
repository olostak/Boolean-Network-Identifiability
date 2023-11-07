import unittest
import asynchronose_boolaen_networks as ABN

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
        self.assertEqual(ABN.get_stable_values(timeseries), expected)

    def test_add_path_to_graph(self):
        graph = ABN.TransitionGraph()
        state = [0, 0, 0]
        path = [1, 2, 0]
        ABN.add_path_to_graph(graph, state, path)
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
        value = ABN.check_path_respect_stable(changes, state, stable)
        self.assertTrue(value)

    def test_check_path_respect_stable_false(self):
        state = [0, 1]
        changes = [1, 0]
        stable = [
            ([0, 0], 0, 0),
            ([1, 0], 0, 1),
            ([1, 1], 0, 1),
        ]
        value = ABN.check_path_respect_stable(changes, state, stable)
        self.assertFalse(value)

    def test_check_path_respect_stable_false2(self):
        state = [1, 0]
        changes = [0, 1]
        stable = [
            ([0, 0], 1, 0),
            ([1, 1], 1, 1),
            ([1, 1], 0, 1),
        ]
        value = ABN.check_path_respect_stable(changes, state, stable)
        self.assertFalse(value)

    def test_get_truth_table(self):
        graph = ABN.TransitionGraph()
        graph.add_transition([0, 0], [0, 1], 1)
        graph.add_transition([0, 1], [1, 1], 0)
        graph.add_transition([1, 1], [1, 0], 1)
        graph.add_transition([1, 0], [1, 1], 1)

        expected_truth_table = [
            ('[0, 0]', '[0, 1]'),
            ('[0, 1]', '[1, 1]'),
            ('[1, 1]', '[1, 0]'),
            ('[1, 0]', '[1, 1]')
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

        graph = ABN.transition_graph_construction(timeseries)
        expected_truth_table = [
                ('[0, 0]', '[0, 1]'),
                ('[0, 1]', '[1, 1]'),
                ('[1, 1]', '[1, 0]'),
                ('[1, 0]', '[1, 1]')
            ]
        self.assertEqual(graph.get_truth_table(), expected_truth_table)

    def test_non_existing_transision_graph(self):
        timeseries = [
            ([0, 0],[1, 0]),
            ([0, 1],[1, 0]),
            ([1, 0],[0, 1]),
            ([1, 1],[1, 1]),
        ]

        graph = ABN.transition_graph_construction(timeseries)
        expected_truth_table = []
        self.assertEqual(graph.get_truth_table(), expected_truth_table)





# This is the entry point for running the tests
if __name__ == '__main__':
    unittest.main()