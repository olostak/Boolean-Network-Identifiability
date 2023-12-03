from . import matrics_utils

def run_benchmark(model_original, model_submitted):
    tp, _, _, fn = matrics_utils.get_true_false_positive_negative(model_original, model_submitted)
    return (tp ) / (tp + fn)