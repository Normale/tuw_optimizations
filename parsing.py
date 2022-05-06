import networkx as nx
from line_graph import convert_to_line_graph
def read_graph(filepath):
    """
    Function reading a graph file and creating a graph from it.
    """
    graph = nx.DiGraph()
    with open(filepath) as f:
        for _ in range(6):
            next(f)
        for line in f:
            if "coste" not in line: break
            v_string, e_string = line.split('coste')
            vertices = v_string.split(',')
            vertices = list(map(lambda x: int(''.join(c for c in x if c.isdigit())), vertices))
            edges = [int(x) for x in e_string.split(' ') if len(x) > 0]
            graph.add_nodes_from(vertices)
            graph.add_edge(vertices[0], vertices[1], weight=edges[0])
            graph.add_edge(vertices[1], vertices[0], weight=edges[1])
    distances = nx.all_pairs_dijkstra_path_length(graph, weight="weight")
    distances_dict = dict(list(distances))
    paths = nx.all_pairs_dijkstra_path(graph, weight="weight")
    paths = dict(list(paths))
    return graph

def get_graph_dict(graph: nx.Graph):
    distances = nx.all_pairs_dijkstra_path_length(graph, weight="weight")
    distances_dict = dict(list(distances))
    paths = nx.all_pairs_dijkstra_path(graph, weight="weight")
    paths = dict(list(paths))
    return {"graph": graph, "distances": distances_dict, "paths": paths}

if __name__ == '__main__':
    g1 = read_graph("instances\\toy")
    line_g1 = convert_to_line_graph(g1)
    result = get_graph_dict(line_g1)
    g, distances, paths = result["graph"], result["distances"], result["paths"]
    print(distances[(1,2)][(2,3)]) # distance from (1,2) to (2,3)
    print(paths[(1,2)][(2,3)]) # path from (1,2) to (2,3)
