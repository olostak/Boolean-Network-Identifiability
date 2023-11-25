from  . import matrics_utils

def run_benchmark(bn_original, bn_infered):
    graph_original = bn_original.graph()
    graph_submitted = bn_infered.graph()

    igraph_original = matrics_utils.regulatory_to_igraph(graph_original)
    igraph_submitted = matrics_utils.regulatory_to_igraph(graph_submitted)

    s_paths_original = igraph_original.distances()
    s_paths_submitted = igraph_submitted.distances()

    return matrics_utils.compare_matrix(s_paths_original, s_paths_submitted)