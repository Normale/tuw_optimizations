import networkx as nx
from line_graph import convert_to_line_graph
from tsp import tsp
from parsing import get_graph_dict, read_graph

def wpp(graph):
    nodes, line_g = convert_to_line_graph(graph)
    line_distances = get_graph_dict(line_g)["distances"]

    sequence, distance = tsp(line_distances)
    print(sequence)
    print(nodes)

    wpp_path = []

    prev = -1
    non_common = -1
    for i in range(len(sequence) - 1):
        from_node = nodes[sequence[i]]
        to_node = nodes[sequence[i + 1]]
        print(i)
        common = (set(from_node) & set(to_node)).pop()  # common vertice of two edges
        if (prev == common):
            wpp_path.append(non_common.pop())
        non_common = set(from_node) | set(to_node)
        non_common.discard(common)
        non_common.discard(prev)
        wpp_path.append(common)
        prev = common

    print_solution(wpp_path, distance)

def print_solution(wpp_path, distance):
    out_string = 'Best route:\n'
    for node in wpp_path:
        out_string += str(node) + " -> "
    out_string += '1\n'
    out_string += 'Distance of the route: {}'.format(distance)
    print(out_string)

if __name__ == '__main__':
    wpp(read_graph("instances\\toy"))

    """
    # Dummy example discussed
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

    wpp(graph)

    # The following two are not found, KeyError is raised, because the line graph nodes are uniformised to have the lower indexed node first (2,3 instead of 3,2)
    #print(distances[(1,2)][(3,2)])
    #print(distances[(3,2)][(1,2)])
    """