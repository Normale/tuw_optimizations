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
    print(distances[(1,2)][(2,3)])
    print(distances[(2,3)][(1,2)]) 
    print(paths[(1,2)][(2,3)]) # path from (1,2) to (2,3)


    # Dummy example discussed
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
    line_g = convert_to_line_graph(graph)
    result = get_graph_dict(line_g)
    g, distances, paths = result["graph"], result["distances"], result["paths"]
    print(distances[(1,2)][(2,3)])
    print(distances[(2,3)][(1,2)]) 
    # The following two are not found, KeyError is raised
    #print(distances[(1,2)][(3,2)])
    #print(distances[(3,2)][(1,2)])