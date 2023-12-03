from . import attractor_count as benchmark_attractor_count
from . import shortest_path as benchmark_shortest_path
from . import truth_tables as benchmark_truth_tables
from . import accuracy as benchmark_accuracy
from . import precision as benchmark_precision
from . import recall as benchmark_recall
from . import f1_score as benchmark_f1
from . import in_degree_similarity as benchmark_in_degree
from . import matrics_utils

all_benchmarks = {
    "Attractor count": benchmark_attractor_count,
    "Shortest path": benchmark_shortest_path,
    "Truth tables": benchmark_truth_tables,
    "Accuracy": benchmark_accuracy,
    "Precision": benchmark_precision,
    "Recall": benchmark_recall,
    "F1 score": benchmark_f1,
    "In-degree similarity": benchmark_in_degree,
}