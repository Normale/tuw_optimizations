import networkx as nx


def convert_to_line_graph(g: nx.Graph):
    L = nx.line_graph(g)
    L2 = nx.DiGraph()
    for l_edge in L.edges():
        src, dest = l_edge
        if src == dest[::-1]:
            continue
        # edges 0-2 and 2-0 are different for networkx, but we treat them as the same
        if (
            L2.has_edge(src, dest)
            or L2.has_edge(src, dest[::-1])
            or L2.has_edge(src[::-1], dest)
            or L2.has_edge(src[::-1], dest[::-1])
        ):
            continue
        L2.add_node(src)
        L2.add_node(dest)
        common = (set(src) & set(dest)).pop()  # common vertice of two edges
        other_s = src[0] if common == src[1] else src[1]
        other_d = dest[0] if common == dest[1] else dest[1]
        w1 = g.get_edge_data(other_s, common)["weight"]
        if g.degree(other_d) != 2:  # degree = 2 - > 1 incoming, 1 outgoing edge
            w2 = g.get_edge_data(other_d, common)["weight"]
        else:
            w2 = (
                g.get_edge_data(other_d, common)["weight"]
                + g.get_edge_data(common, other_d)["weight"]
            )
        L2.add_edge(src, dest, weight=w1)
        L2.add_edge(dest, src, weight=w2)
    return L2


def map_edge(edge):
    if edge == (0, 1) or edge == (1, 0):
        return "X"
    if edge == (1, 2) or edge == (2, 1):
        return "Y"
    if edge == (2, 3) or edge == (3, 2):
        return "V"
    if edge == (0, 2) or edge == (2, 0):
        return "Z"


if __name__ == "__main__":
    graph = nx.DiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, weight=4)
    graph.add_edge(1, 0, weight=3)
    graph.add_edge(0, 2, weight=1)
    graph.add_edge(2, 0, weight=2)
    graph.add_edge(1, 2, weight=5)
    graph.add_edge(2, 1, weight=6)
    graph.add_edge(2, 3, weight=3)
    graph.add_edge(3, 2, weight=5)
    g2 = convert_to_line_graph(graph)

    for e1, e2, data in g2.edges(data="weight"):
        e1str, e2str = map_edge(e1), map_edge(e2)
        print(f"{e1str} -> {e2str} == {data}")
    print(g2.edges(data=True))
