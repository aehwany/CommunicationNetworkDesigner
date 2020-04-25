import edge_generator
import itertools
from network_solver import NetworkSolver
from edge import Edge

def getTotalCost(list):
    i = 0
    cost = 0
    for i in range(len(list)):
        cost += list[i].cost
    return cost

def main():
    try:
        # file_path = input("Please set input file path: ")
        # rbGoal = input("Please enter reliability goal: ")
        # costGoal = input("Please enter cost constraint: ")
        # modeA = input("run Mode A) Meet given Relability? (y/n) ")
        # modeB = input("run Mode B) Max reliability given cost? (y/n) ")
        file_path = "input.txt"
        rbGoal = 1.5
        costGoal = 300
        modeA="n"
        modeB="y"

    except Exception as e:
        print(e)
        exit()
    print("-----"*10)
    print("Reliability goal= " + str(rbGoal))
    print("Cost constraint= " + str(costGoal))

    nodesCount, reliability, cost = edge_generator.read_data(file_path)
    city_list, edge_list = edge_generator.generate(file_path)

    edge_list.sort(key=lambda x: x.reliability, reverse=True)
    networkSolver = NetworkSolver(edge_list, nodesCount, rbGoal, costGoal)

    if modeA=="Y" or modeA=="y":
        execute_mode_A(networkSolver)
    if modeB=="Y" or modeB=="y":
        execute_mode_B(networkSolver)

def execute_mode_A(networkSolver):
    print("running mode A")
    reliability = networkSolver.get_total_reliability(networkSolver.edge_list, networkSolver.number_of_cities)
    if reliability >= networkSolver.reliability_goal:
        print("Results of graph that meets the specified Reliability Goal: ")
        print("Total Reliability= " + str(reliability))
        print("Total Cost= " + str(networkSolver.get_total_cost(networkSolver.edge_list)))
        print(networkSolver.edge_list)
    else:
        print("No design found that meets the specified Reliability Goal")


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