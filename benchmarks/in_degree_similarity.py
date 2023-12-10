def run_benchmark(bn_original, bn_infered):
    graph_original = bn_original.graph()
    graph_submitted = bn_infered.graph()

    variables = graph_original.variables()
    sum = 0
    for variable in variables:
        original_regurators = graph_original.regulators(variable)
        submitted_regulators = graph_submitted.regulators(variable)
        sum += 1 - (abs(len(original_regurators) - len(submitted_regulators)) / len(variables))
    return round(sum / len(variables) * 100)