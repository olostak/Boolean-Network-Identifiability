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