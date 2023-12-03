import re
from pathlib import Path
from biodivine_aeon import *
from itertools import permutations, product

def __replace_nonelementar_operations_expression(match):
        a, b = match.group(1), match.group(3)
        operation = match.group(2)

        if operation == 'xor':
            return f"({b} and int( not {a})) or ( int( not {b}) and {a})"
        elif operation == 'nand':
            return f"int( not ({a} and {b}))"
        elif operation == 'nor':
            return f"int( not ({a} or {b}))"
        else:
            return match.group()
        
        
def __replace_nonelementar_operations(match):
        a, b = match.group(1), match.group(3)
        operation = match.group(2)

        if operation == 'xor':
            return f"({b} & !{a}) | (!{b} & {a})"
        elif operation == 'nand':
            return f"!{a} | !{b}"
        elif operation == 'nor':
            return f"!{a} & !{b}"
        else:
            return match.group()
        

# Example string
expression = "!var_0 nor !var_2 xor !var_3"

# Regex pattern
pattern = r'(!?\([^)]*\)|[^\s()]+)\s+(xor)\s+(!?\([^)]*\)|[^\s()]+)'
expression = re.sub(r'(!?\([^)]*\)|[^\s()]+)\s+(xor)\s+(!?\([^)]*\)|[^\s()]+)',
                    __replace_nonelementar_operations,
                    expression)
expression = re.sub(pattern, __replace_nonelementar_operations, expression, count=0)
expression = re.sub(r'(!?\([^)]*\)|[^\s()]+)\s+(nor)\s+(!?\([^)]*\)|[^\s()]+)',
                    __replace_nonelementar_operations,
                    expression)
expression = re.sub(r'(!?\([^)]*\)|[^\s()]+)\s+(nand)\s+(!?\([^)]*\)|[^\s()]+)',
                    __replace_nonelementar_operations,
                    expression)
cleaned_expr = re.sub(r'!!', '', expression)

print(cleaned_expr)


"""def invert_negations_in_brackets(expr):
    # Regex pattern to find negated expressions within brackets
    pattern = r'!\((.*)\)'

    # Function to invert negations within the matched expression
    def invert(match):
        inner_expr = match.group(1)
        # Invert negation of each variable in the matched expression
        return '(' + re.sub(r'!?var_\d+', lambda var: var.group().lstrip('!') if var.group().startswith('!') else '!' + var.group(), inner_expr) + ')'
    
    # Apply the inversion to all matched expressions
    while True:
        new_expr, n = re.subn(pattern, lambda m: '(' + invert(m) + ')', expr)
        if n == 0:  # No more replacements, exit the loop
            break
        expr = new_expr

    return expr

# Example usage
input_expr = "!(!(var_0 & !var_3) & var_2)"
output_expr = invert_negations_in_brackets(input_expr)
print(output_expr)

def invert_negations_in_brackets(expr):
    stack = []  # Stack to keep track of '(' positions
    inverted = []  # List to store inverted expressions
    i = 0

    while i < len(expr):
        if expr[i] == '!':
            if i + 1 < len(expr) and expr[i + 1] == '(':
                stack.append((i, True))  # Store index and negation flag
                i += 1  # Skip '!'
        elif expr[i] == '(' and not stack:
            stack.append((i, False))  # Store index without negation flag
        elif expr[i] == ')':
            if stack:
                start, negate = stack.pop()
                if negate:
                    # Invert negations inside this bracket pair
                    inner_expr = expr[start + 2:i]  # Exclude '!(' and ')'
                    inverted_expr = re.sub(r'!?var_\d+', lambda var: '!' + var.group().lstrip('!') if var.group().startswith('!') else var.group().lstrip('!'), inner_expr)
                    inverted.append((start, i + 1, f"({inverted_expr})"))
        i += 1

    # Apply the inverted expressions
    for start, end, replacement in reversed(inverted):
        expr = expr[:start] + replacement + expr[end:]

    return expr

# Example usage
input_expr = "!(var_0 & !(var_1 & var_2) & !var_3) & var_4"
output_expr = invert_negations_in_brackets(input_expr)
print(output_expr)"""


import re
from collections import defaultdict

def identify_variable_negation(expr):
    pattern = r'!?(var_\d+)'
    var_occurrences = defaultdict(lambda: {'negated': False, 'positive': False})
    for match in re.finditer(pattern, expr):
        var = match.group(1)
        is_negated = match.group(0).startswith('!')
        if is_negated:
            var_occurrences[var]['negated'] = True
        else:
            var_occurrences[var]['positive'] = True

    negated = [var for var, types in var_occurrences.items() if types['negated'] and not types['positive']]
    positive = [var for var, types in var_occurrences.items() if types['positive']and not types['negated']]
    both_forms = [var for var, types in var_occurrences.items() if types['negated'] and types['positive']]

    return positive, negated, both_forms

# Example usage
input_expr = "(!var_0 & var_2) | (var_0 & !var_2) & var_3 | !var_4"
positive, negated, both_forms = identify_variable_negation(input_expr)
print(positive)
print(negated)
print(both_forms)


original_string = Path(f"./evaluate/original.aeon").read_text()
bn_original = BooleanNetwork.from_aeon(original_string)

submitted_string = Path(f"./evaluate/cell_division/infered.aeon").read_text()
bn_submitted = BooleanNetwork.from_aeon(submitted_string)

pattern_not = r'!v_(\d+)'
pattern = r'v_(\d+)'
expression = "(((v_0 & !v_1) & !v_4) & v_3)"

expression = re.sub(pattern_not, r'int( not {\1})', expression)
expression = re.sub(pattern, r'int({\1})', expression)
for p in product((True, False), repeat=5):
     print(list(p))
     print(eval(expression.format(*list(p))))
print(expression)

     

     
