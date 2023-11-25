import biodivine_aeon
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import And, Or, Not, Implies, Xnor, simplify_logic, truth_table


def run_benchmark(model_original, model_submitted):

    # We are assuming all the variables are included in both models
    variables_original = list(map(lambda v: model_original.get_variable_name(v), model_original.variables()))

    scores = {}

    for variable in variables_original:
        function_original = model_original.get_update_function(variable)
        function_submitted = model_submitted.get_update_function(variable)

        score = compare_functions(str(function_original), str(function_submitted), variables_original)
        scores[variable] = score

    avg = 0
    for variable, score in scores.items():
        avg += score
    avg /= len(scores)

    return avg


def compare_functions(function_original, function_submitted, model_vars):

    function_original = function_original.replace("!", "~")
    function_submitted = function_submitted.replace("!", "~")

    equiv_results = []

    expr_original = simplify_logic(function_original)
    expr_submitted = simplify_logic(function_submitted)

    table_original = list(truth_table(expr_original, model_vars))
    table_submitted = list(truth_table(expr_submitted, model_vars))

    for row in range(0, len(table_original)):
        value_original = table_original[row][-1]
        value_submitted = table_submitted[row][-1]

        equiv_results.append(value_submitted == value_original)

    true_count = sum(equiv_results)
    total_count = len(equiv_results)
    rating = round(true_count / total_count * 100)

    return rating