import networkx as nx
from simulated_annealing import anneal
from line_graph import convert_to_line_graph
from tsp import tsp
from parsing import get_graph_dict, read_graph

import timeit
from functools import wraps

def timer(function):
    @wraps(function)
    def wrapper_timer(*args, **kwargs):
        start_time = timeit.default_timer()
        value = function(*args, **kwargs)
        elapsed = timeit.default_timer() - start_time
        print(f'Function "{function.__name__}" took {elapsed} seconds to complete.')
        return value
    return wrapper_timer

@timer
def wpp(graph):
    nodes, line_g = convert_to_line_graph(graph)
    graph_dict = get_graph_dict(line_g)
    line_distances = graph_dict["distances"]
    paths = graph_dict["paths"]
    sequence, distance = tsp(line_distances)

    line_solution = []
    for i in range(len(sequence) - 1):
        from_id = sequence[i]
        to_id = sequence[i + 1]

        subpath_ids = paths[from_id+1][to_id+1]

        if line_solution and subpath_ids[0] == line_solution[-1]:
            line_solution.pop()
        line_solution.extend(subpath_ids)
    # print_solution(line_solution, distance)
    solution = from_linegraph_to_normal(line_solution, nodes)

    # Final solution of simulated annealing
    final_solution, final_score = anneal(graph, solution, distance)
    return final_solution, final_score

def from_linegraph_to_normal(path, nodes):
    vertice_path = []
    for i in range(len(path) - 1):
        node = path[i]
        next_node = path[i+1]
        src = nodes[node - 1]
        dest = nodes[next_node - 1]        
        common = (set(src) & set(dest)).pop() 
        other_d = dest[0] if common == dest[1] else dest[1]
        vertice_path.append(common)
        vertice_path.append(other_d)
    result = []
    for i in range(len(vertice_path)):
        if i > 0 and vertice_path[i] == vertice_path[i - 1]:
            continue
        result.append(vertice_path[i])
    # print("View of original vertices: ")
    # print(' -> '.join(str(x) for x in result))
    return result

def print_solution(wpp_path, distance):
    out_string = 'WPP route:\n'
    for node in wpp_path:
        out_string += str(node) + " -> "
    out_string += '1\n'
    out_string += 'Distance of the route: {}'.format(distance)
    # print(out_string)

if __name__ == '__main__':
    
    import os
    for f in sorted(os.listdir("instances"))[1:10]:
        fpath = os.path.join("instances", f)
        print(fpath)
        wpp(read_graph(fpath))
    
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
    """

    # # The following two are not found, KeyError is raised, because the line graph nodes are uniformised to have the lower indexed node first (2,3 instead of 3,2)
    # #print(distances[(1,2)][(3,2)])
    # #print(distances[(3,2)][(1,2)])
    