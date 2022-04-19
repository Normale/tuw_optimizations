from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from parsing import read_graph

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
    out_string += 'Distance of the route: {}\n'.format(route_distance)
    print(out_string)

def define_distance(distances, manager):
    def distance(initial, final):
        from_node = manager.IndexToNode(initial)
        to_node = manager.IndexToNode(final)
        return distances[from_node + 1][to_node + 1]
    return distance

def setup(instance):
    # Create the routing index manager.
    distances = read_graph("instances\\" + instance)["distances"]
    manager = pywrapcp.RoutingIndexManager(len(distances), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    
    distance = define_distance(distances, manager)
    arcCostEvaluator = routing.RegisterTransitCallback(distance)
    routing.SetArcCostEvaluatorOfAllVehicles(arcCostEvaluator)

    return manager, routing

def main(instance):
    manager, routing = setup(instance)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        print_solution(manager, routing, assignment)

if __name__ == '__main__':
    main("toy")