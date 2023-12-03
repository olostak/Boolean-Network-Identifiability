from benchmarks import benchmark_recall, benchmark_precision 


def run_benchmark(model_original, model_submitted):
    precision = benchmark_precision.run_benchmark(model_original, model_submitted)
    recall = benchmark_recall.run_benchmark(model_original, model_submitted)
    return 2 * ((precision * recall) / (precision + recall))