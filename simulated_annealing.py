from numpy import random
from mpmath import exp
import networkx as nx

def evaluate(graph, solution):
    score = 0
    for i in range(len(solution) - 1):
        n_start = solution[i]
        n_end = solution[i + 1]
        score += graph.edges[n_start,n_end]["weight"]
    return score

def mutate(solution):
    # Check for repeated nodes
    node_occs = dict()
    for i in range(len(solution)):
        if solution[i] not in node_occs:
            node_occs[solution[i]] = [i]
        else:
            node_occs[solution[i]] = node_occs[solution[i]] + [i]
    # print("Node occurrences:", node_occs)

    # Check which of these nodes has cycle(s)
    cycles = []
    for i in range(len(node_occs)):
        id, indexes = list(node_occs.items())[i]
        for j in range(len(indexes) - 1):
            if (indexes[j + 1] - indexes[j] > 2):
                cycles.append(id)
                break
    # print("Nodes with cycles:", cycles)

    # Pick random node with cycle
    selected = cycles[random.randint(0, len(cycles) - 1)]
    indexes = node_occs[selected]
    # print("Selected:", selected)

    # Pick a random cycle from selected node
    options = []
    for i in range(len(indexes) - 1):
        if indexes[i + 1] - indexes[i] > 2:
            options.append(indexes[i])
    # print("Options:", options)
    if (len(options) > 0):
        index = random.choice(options)
    # print("Index:", index)

    # Switch direction of the cycle
    new_solution = []
    cycle = []
    terminated = False

    for i in range(len(solution)):
        if (i > index and not terminated):
            if (solution[i] == solution[index]):
                terminated = True
                for _ in range(len(cycle)):
                    new_solution.append(cycle.pop())
                new_solution.append(solution[i])
            else:
                cycle.append(solution[i])
        else:
            new_solution.append(solution[i])
    return new_solution

def cooldown(init_temperature, iteration):
    return init_temperature / (1 + iteration ** 2)

def anneal(graph, solution, score):
    # Print original solution and score
    # print("Original solution:", solution)
    # print("Score:", score)

    n_mutation = 1
    # Save initial solution as best
    best_solution = solution
    best_score = score

    # Initiate temperature
    init_temperature = 100

    # Mutate until 20 consecutive iterations without improvement
    while (n_mutation <= 10):
        # Cooldown temperature
        temperature = cooldown(init_temperature, n_mutation)

        # Current solution must be saved in each iteration
        curr_solution = solution
        curr_score = score

        # Create mutation and calculate score
        mut_solution = mutate(curr_solution)
        mut_score = evaluate(graph, mut_solution)
        # print("Solution after mutation:", mut_solution)
        # print("Score:", mut_score)

        # If score is higher than the current best, replace and reset iterations
        if (mut_score < best_score):
            best_score = mut_score
            best_solution = mut_solution
            n_mutation = 0
        
        # If score is higher than the current solution or random factor is smaller than epsilon, replace
        if (mut_score < curr_score or exp((mut_score - curr_score)/temperature) >= random.random()):
            curr_score = mut_score
            curr_solution = mut_solution

        # Increment iteration number
        n_mutation += 1

    print_sim(best_solution, best_score)
    
    return best_solution, best_score

def print_sim(solution, score):
    out_string = ''
    # out_string = 'Best route:\n' + str(solution[0])
    # for node in solution[1:]:
    #     out_string += " -> " + str(node)
    out_string += '\nDistance of the route: {}'.format(score)
    print(out_string)

if __name__ == '__main__':
    # For testing effects
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4])
    graph.add_edge(1, 3, weight=10)
    graph.add_edge(3, 1, weight=1)
    graph.add_edge(1, 4, weight=1)
    graph.add_edge(4, 1, weight=13)
    graph.add_edge(2, 3, weight=1)
    graph.add_edge(3, 2, weight=15)
    graph.add_edge(2, 4, weight=16)
    graph.add_edge(4, 2, weight=1)
    graph.add_edge(3, 4, weight=18)
    graph.add_edge(4, 3, weight=19)
    print(anneal(graph,[1,3,4,1,3,2,4,1], evaluate(graph, [1,3,4,1,3,2,4,1])))