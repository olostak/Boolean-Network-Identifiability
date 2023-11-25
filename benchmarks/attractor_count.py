import biodivine_aeon
from . import matrics_utils

def run_benchmark(model_original, model_submitted):

    stg_original = biodivine_aeon.SymbolicAsyncGraph(model_original)
    stg_submitted = biodivine_aeon.SymbolicAsyncGraph(model_submitted)

    attractors_original = biodivine_aeon.find_attractors(stg_original)
    attractors_submitted = biodivine_aeon.find_attractors(stg_submitted)

    amount_original = len(attractors_original)
    amount_submitted = len(attractors_submitted)

    amount_rating = matrics_utils.arbitrary_rating(amount_original, amount_submitted)

    class_counts_original = count_attractor_types(stg_original, attractors_original)
    class_counts_submitted = count_attractor_types(stg_submitted, attractors_submitted)

    counts_rating = compare_counts(class_counts_original, class_counts_submitted)

    return (amount_rating + counts_rating) / 2


def count_attractor_types(stg, attractors):
    counted = {"stability": 0, "oscillation": 0, "disorder": 0}

    for attractor in attractors:
        classes = biodivine_aeon.classify_attractor(stg, attractor)

        if "stability" in classes:
            counted["stability"] += 1
        elif "oscillation" in classes:
            counted["oscillation"] += 1
        elif "disorder" in classes:
            counted["disorder"] += 1

    return counted


def compare_counts(counts_original, counts_submitted):
    ratings = []

    for cls in ["stability", "oscillation", "disorder"]:
        count_original = counts_original[cls]
        count_submitted = counts_submitted[cls]

        ratings.append(matrics_utils.arbitrary_rating(count_original, count_submitted))

    return sum(ratings) / len(ratings)