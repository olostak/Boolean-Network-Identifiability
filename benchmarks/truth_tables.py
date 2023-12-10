from sympy.logic.boolalg import simplify_logic, truth_table
import re
from itertools import product


def run_benchmark(model_original, model_submitted):

    # We are assuming all the variables are included in both models
    variables_original = list(map(lambda v: model_original.get_variable_name(v), model_original.variables()))

    scores = {}

    for variable in variables_original:
        try: 
            function_original = model_original.get_update_function(variable)
            function_submitted = model_submitted.get_update_function(variable)

            score = compare_functions(str(function_original), str(function_submitted), variables_original)
            scores[variable] = score
        except:
            pass

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
    expression = expression.replace('!', ' not ')
    numbers = [int(num) for num in re.findall(r'\d+', expression)]

    # Get unique numbers and sort them
    unique_sorted_numbers = sorted(set(numbers))

    max_number = max(unique_sorted_numbers)

    # Create a dictionary to map each number to its rank
    number_to_rank = {number: rank for rank, number in enumerate(unique_sorted_numbers)}

    # Replace each number in the text with its rank
    for number in unique_sorted_numbers:
        expression = expression.replace(str(number), str(number_to_rank[number]))
    return expression, max_number


def compare_functions(function_original, function_submitted, model_vars):
    """function_original = function_original.replace("!", "~")
    function_submitted = function_submitted.replace("!", "~")

    equiv_results = []

    expr_original = simplify_logic(function_original)
    expr_submitted = simplify_logic(function_submitted)

    table_original = list(truth_table(expr_original, model_vars))
    table_submitted = list(truth_table(expr_submitted, model_vars))

    for row in range(0, len(table_original)):
        value_original = table_original[row][-1]
        value_submitted = table_submitted[row][-1]

        equiv_results.append(value_submitted == value_original)"""
    expression_original, max_original = get_expression(function_original)
    expression_submitted, max_sumitted = get_expression(function_submitted)
    
    max_regulators = max(max_original, max_sumitted)
    total_count = 0
    true_count = 0
 
    for p in product((True, False), repeat=max_regulators):
        if eval(expression_original.format(*list(p))) == eval(expression_submitted.format(*list(p))):
            true_count += 1
        total_count += 1
    return round(true_count / total_count * 100)