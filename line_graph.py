import networkx as nx
import matplotlib.pyplot as plt

def convert_to_line_graph(g: nx.Graph):
    L = nx.line_graph(g)
    L2 = nx.DiGraph()
    for l_edge in L.edges():
        src, dest = l_edge
        L2.add_node(src)
        L2.add_node(dest)
        w1 = g.get_edge_data(dest[0], dest[1])
        w2 = g.get_edge_data(dest[1], dest[0])
        L2.add_edge(src, dest, weight=w1)
        L2.add_edge(dest, src, weight=w2) 
    return L2


if __name__ == '__main__':
    graph = nx.Graph()
    graph.add_nodes_from([0,1,2,3])
    graph.add_edge(0, 1, weight=4)
    graph.add_edge(1, 0, weight=3)
    graph.add_edge(0, 2, weight=1)
    graph.add_edge(2, 0, weight=2)
    graph.add_edge(1, 2, weight=6)
    graph.add_edge(2, 1, weight=5)
    graph.add_edge(3, 2, weight=5)
    graph.add_edge(2, 3, weight=3)
    g2 = convert_to_line_graph(graph)
    print(g2.edges(data="weight"))
