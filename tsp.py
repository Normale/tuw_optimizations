from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from parsing import read_graph, get_graph_dict

def print_solution(manager, routing, assignment):
    index = routing.Start(0)
    out_string = 'Best route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        out_string += '{} -> '.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    out_string += '{}\n'.format(manager.IndexToNode(index))
    out_string += 'Distance of the route: {}'.format(route_distance)
    print(out_string)

def solution(routing, assignment):
    sequence = []
    index = routing.Start(0)
    route_distance = 0
    while not routing.IsEnd(index):
        sequence.append(index)
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    sequence.append(0)
    return sequence, route_distance

def define_distance(distances, manager):
    def distance(initial, final):
        from_node = manager.IndexToNode(initial)
        to_node = manager.IndexToNode(final)
        return distances[from_node + 1][to_node + 1]
    return distance

def setup(distances):
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(distances), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    
    distance = define_distance(distances, manager)
    arcCostEvaluator = routing.RegisterTransitCallback(distance)
    routing.SetArcCostEvaluatorOfAllVehicles(arcCostEvaluator)

    return manager, routing

def tsp(distances):
    manager, routing = setup(distances)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        # print_solution(manager, routing, assignment)
        return solution(routing, assignment)

def tsp2(distances):
    manager, routing = setup(distances)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
    search_parameters.time_limit.seconds = 30

    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        print_solution(manager, routing, assignment)
        return solution(routing, assignment)

if __name__ == '__main__':
    tsp(get_graph_dict(read_graph("instances\\toy"))["distances"])