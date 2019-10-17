def make_edge(node_a, node_b, weight):
    nodes_list = sorted([node_a, node_b])
    return (nodes_list[0], nodes_list[1], weight)