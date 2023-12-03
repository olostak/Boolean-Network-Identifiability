from sympy.logic.boolalg import simplify_logic, truth_table
import re
from itertools import product


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

def get_expression(function):
    pattern_not = r'!v_(\d+)'
    pattern = r'v_(\d+)'
    expression = re.sub(pattern_not, r'int( not {\1})', function)
    expression = re.sub(pattern, r'int({\1})', expression)
    return expression


def compare_functions(function_original, function_submitted, model_vars):
    expression_original = get_expression(function_original)
    expression_submitted = get_expression(function_submitted)
    
    total_count = 0
    true_count = 0
    for p in product((True, False), repeat=len(model_vars)):
        if eval(expression_original.format(*list(p))) == eval(expression_submitted.format(*list(p))):
            true_count += 1
        total_count += 1
    rating = round(true_count / total_count * 100)

    return rating