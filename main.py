import edge_generator
from network_solver import NetworkSolver

def main():
    try:
        file_path = input("Please set input file path: ")
        rbGoal = input("Please enter reliability goal: ")
        costGoal = input("Please enter cost constraint: ")
        modeA = input("run Mode A) Meet given Relability? (y/n) ")
        modeB = input("run Mode B) Max reliability given cost? (y/n) ")

    except Exception as e:
        print(e)
        exit()
    print("-----"*10)
    print("Reliability goal= " + str(rbGoal))
    print("Cost constraint= " + str(costGoal))
    print("-----"*10)

    nodesCount, reliability, cost = edge_generator.read_data(file_path)
    city_list, edge_list = edge_generator.generate(file_path)

    edge_list.sort(key=lambda x: x.reliability, reverse=True)
    networkSolver = NetworkSolver(edge_list, int(nodesCount), float(rbGoal), int(costGoal))

    if modeA=="Y" or modeA=="y":
        execute_mode_A(networkSolver)
    if modeB=="Y" or modeB=="y":
        execute_mode_B(networkSolver)

def execute_mode_A(networkSolver):
    print("running mode A")
    reliability = networkSolver.get_total_reliability(networkSolver.edge_list, networkSolver.number_of_cities)
    if reliability >= networkSolver.reliability_goal:
        print("Result of graph meets the specified Reliability Goal: ")
        print("Total Reliability= " + str(reliability))
        print("Total Cost= " + str(networkSolver.get_total_cost(networkSolver.edge_list)))
        print(networkSolver.edge_list)
    else:
        print("No design found that meets the specified Reliability Goal")
    print("\n")


def execute_mode_B(networkSolver):
    print("running mode B")
    accepted_cost_solutions = networkSolver.meets_cost_constraint()
    if(len(accepted_cost_solutions)>0):
        val, graph = networkSolver.find_max_reliability(accepted_cost_solutions, networkSolver.number_of_cities)
        print("Total Reliability= " + str(val))
        print("Total Cost= " + str(networkSolver.get_total_cost(graph)))
        print(graph)
        print("\n")
    else:
        print("No design found that meets the given cost constraint")


if __name__ == "__main__":
    main()