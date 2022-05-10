import networkx as nx
from parsing import read_graph

def convert_to_line_graph(g: nx.Graph):
    L = nx.line_graph(g)
    L2 = nx.DiGraph()
    for l_edge in L.edges():
        src, dest = l_edge
        # uniformising nodes of the line graph to have lower first node
        if src[0] > src[1]:
            src = (src[1], src[0])
        if dest[0] > dest[1]:
            dest = (dest[1], dest[0])
            
        if src == dest:
            continue
        # edges 0-2 and 2-0 are different for networkx, but we treat them as the same
        if (
            L2.has_edge(src, dest)
            or L2.has_edge(dest, src)
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

    L3 = nx.DiGraph()
    for i in range(len(L2.nodes)):
        L3.add_node(i + 1)

    nodes = list(L2)

    for edge in L2.edges:
        w = L2[edge[0]][edge[1]]["weight"]
        L3.add_edge(nodes.index(edge[0]) + 1, nodes.index(edge[1]) + 1, weight=w)
        
    return nodes, L3


if __name__ == "__main__":
    nodes, g = convert_to_line_graph(read_graph("instances\\toy"))

    for v1, v2, data in g.edges(data="weight"):
        v1str, v2str = v1, v2
        print(f"Distance {v1str} -> {v2str} = {data}")
    print(g.edges(data=True))

    """
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4])
    graph.add_edge(1, 2, weight=4)
    graph.add_edge(2, 1, weight=3)
    graph.add_edge(1, 3, weight=1)
    graph.add_edge(3, 1, weight=2)
    graph.add_edge(2, 3, weight=5)
    graph.add_edge(3, 2, weight=6)
    graph.add_edge(3, 4, weight=3)
    graph.add_edge(4, 3, weight=5)
    nodes, g2 = convert_to_line_graph(graph)

    def map_vertex(vertex):
        if vertex == 1:
            return "X"
        if vertex == 2:
            return "Y"
        if vertex == 3:
            return "Z"
        if vertex == 4:
            return "V"

    for v1, v2, data in g2.edges(data="weight"):
        v1str, v2str = map_vertex(v1), map_vertex(v2)
        print(f"Distance {v1str} -> {v2str} = {data}")
    print(g2.edges(data=True))
    """
