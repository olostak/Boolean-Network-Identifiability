import igraph

def regulatory_to_igraph(regulatory_graph):
    regulations = regulatory_graph.regulations()
    edges = []

    for regulation in regulations:
        edges.append((regulation["source"], regulation["target"]))

    graph = igraph.Graph.TupleList(edges)

    return graph

def arbitrary_rating(base, measure):
    if base == 0:
        if measure == 0:
            return 100
        else:
            return 0

    if base > measure:
        return (measure / base) * 100

    if measure > 2 * base:
        return 0

    return ((2 * base - measure) / base) * 100

def compare_matrix(original, submitted):

    # Make sure the submitted one has the same number of rows and columns
    # We are expecting the number of variables to be fixed, so the rows and columns must be the same.
    if len(original) != len(submitted):
        return 0

    lengths_original = list(map(len, original))
    lengths_submitted = list(map(len, submitted))

    for i in range(0, len(lengths_original)):
        if lengths_original[i] != lengths_submitted[i]:
            return 0

    ratings_matrix = []
    for i in range(0, len(original)):
        ratings_matrix.append([])
        for j in range(0, len(original[0])):
            rating = arbitrary_rating(original[i][j], submitted[i][j])
            ratings_matrix[i].append(rating)

    row_sums = list(map(sum, ratings_matrix))
    sums = sum(row_sums)

    avg = sums / (len(original) ** 2)

    return avg


def get_true_false_positive_negative(original, submitted):
    graph_original = original.graph()
    graph_submitted = submitted.graph()
    true_positives = 0 #  the number of correctly predicted edges,
    true_negatives = 0 #  the number of correctly predicted non-edges,
    false_positives = 0 # the number of falsely predicted edges,
    false_negatives = 0 # the number of falsely predicted non-edges.

    variables = graph_original.variables()
    for variable in variables:
        original_regurators = graph_original.regulators(variable)
        submitted_regulators = graph_submitted.regulators(variable)
        for variable in variables:
            if variable in original_regurators and variable in submitted_regulators: 
                true_positives += 1
            elif variable not in original_regurators and variable not in submitted_regulators: 
                true_negatives += 1
            elif variable not in original_regurators and variable in submitted_regulators: 
                false_positives += 1
            elif variable in original_regurators and variable not in submitted_regulators:
                false_negatives += 1 
    
    return true_positives, true_negatives, false_positives, false_negatives
    