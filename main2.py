# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator2
import itertools
from edge import Edge


def getTotalCost(list):
    i = 0
    cost = 0
    for i in range(len(list)):
        cost = cost + list[i].cost
    return cost

def getTotalReliability(edge, numOfNodes):
    #Find all possible MST
    combination = list(itertools.product([0, 1], repeat = len(edge)))

    i = 0
    while True:
        if i == (len(combination) - 1):
            break 
        elif sum(combination[i]) < numOfNodes-1:
            del combination[i]
        else:
            i += 1
    
    outputReliability = 0
    for i in range(len(combination)):
        subGraph = []
        for j in range(len(edge)):
            if combination[i][j] == 1: 
                subGraph.append(edge[j])
                 
        if not isAllConnected(subGraph, numOfNodes):
            continue


        subGraphReliability = 1
        for j in range(len(combination[0])):
            if combination[i][j] == 1: 
                subGraphReliability *= edge[j].reliability
            else:
                 subGraphReliability *= (1 - edge[j].reliability)

        outputReliability += subGraphReliability

    return outputReliability

def isAllConnected(edge, numOfNodes):

    # check if all is connected
    connectedNode = []
    # starting from 1
    connectedNode.append(1)
    i = 0
    while i < numOfNodes:
        if len(connectedNode) <= i:
            return False
        if len(connectedNode) == numOfNodes:
            return True
        for x in range(len(edge)):
            
            if edge[x].vertice_1 == connectedNode[i] and edge[x].vertice_2 not in connectedNode: 
                connectedNode.append(edge[x].vertice_2)

            if edge[x].vertice_2 == connectedNode[i] and edge[x].vertice_1 not in connectedNode:
                connectedNode.append(edge[x].vertice_1)
        i += 1



def findMaxReliability(outputFile, graphSet, numOfNodes):
    outputGraph = []
    MaxReli = 0
    for x in range(len(graphSet)):
        if getTotalReliability(graphSet[x], numOfNodes) > MaxReli:
            outputGraph = graphSet[x]
            MaxReli = getTotalReliability(graphSet[x], numOfNodes)

    outputFile.write("\n")

    for x in range(len(outputGraph)):
        outputFile.write("Edge # " + str(x+1) + " : " + str(outputGraph[x].vertice_1) + " - " + str(outputGraph[x].vertice_2) + " Reliability: " + str(outputGraph[x].reliability) + " Cost: " + str(outputGraph[x].cost) + "\n")
    outputFile.write("Total cost: " + str(getTotalCost(outputGraph)) + "\n")
    outputFile.write("Max Reliability " + str(getTotalReliability(outputGraph,numOfNodes)) + "\n")

def meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, costContrained):
    
    # to connect N nodes, we need at least N-1 edges
    # find all combination with N-1 edges (all kind of possible minimal spanning tree)
    combination = list(itertools.product([0, 1], repeat = len(edge)))

    graphSet = []
    i = 0
    while True:
        if i == (len(combination) - 1):
            break 
        elif sum(combination[i]) < numOfNodes-1:
            del combination[i]
        else:
            i += 1

    for i in range(len(combination)):
   
        # declare an empty array to store connected nodes
        connectedNode = []
        offReliability = 1
        
        graph = []
        for j in range(len(edge)):
            if combination[i][j] == 1: 
                graph.append(edge[j])
                 
        if not isAllConnected(graph, numOfNodes):
            continue

        if costContrained and costGoal > 0:
            if getTotalCost(graph) > costGoal:
                continue

        if getTotalReliability(graph, numOfNodes) >= reliabilityGoal:
            graphSet.append(graph)
            # if len(graphSet) == 210:
            #       return graphSet
    return graphSet

def printSolutions(file,sol, numOfNodes):
    for x in range(len(sol)):
        file.write("Solution # " + str(x+1) + "\n")
        file.write("Total reliability:" + str(getTotalReliability(sol[x], numOfNodes)) + "\n")
        for i in range(len(sol[x])):
            file.write("Edge # " + str(i+1) + ": " + str(sol[x][i].vertice_1) + " - " + str(sol[x][i].vertice_2) + " Reliability: " + str(sol[x][i].reliability) + " Cost: " + str(sol[x][i].cost) + "\n")
        file.write("\n")

def decreasingReli(elem):
    return elem.reliability

def main():
    reliabilityGoal = float(input("Please enter reliability goal (from 0 to 1): "))
    costGoal = int(input("Please enter cost constraint (from 1 to 100): "))

    runPartA = input("Would you like to run part A? (y/n)")
    runPartB = input("Would you like to run part B? (y/n)")
    runPartC = input("Would you like to run part C? (y/n)")

    userResponse = []
    for response in [runPartA, runPartB, runPartC]:
        if response == "y" or response == "Y" or response == "yes" or response == "Yes" or response == "YES":
            response = True
        else:
            response = False
        userResponse.append(response)

    print(50 * "*")
    print("Reliability goal set to: " + str(reliabilityGoal))
    print("Cost constraint set to: " + str(costGoal))
    inputValues = edge_generator.readInputFile(userResponse)
    numOfNodes = inputValues[0]
    reliability = inputValues[1]
    cost = inputValues[2]
    edgeNum = inputValues[3]

    edge = [None] * edgeNum
    z = 0
    # Create edge array
    for x in range(numOfNodes):
        for y in range(x + 1, numOfNodes, 1):
            edge[z] = Edge(x+1, y+1, reliability[z], cost[z])
            z = z + 1

    city_list, edge_list = edge_generator.generate()
    edge_list.sort(key=decreasingReli, reverse=True)

    # Execute Part A
    if userResponse[0]:
        outputFileA = open("resultPartA.txt", "a")
        outputFileA.write(50 * "*" + "\n")
        outputFileA.write("PART a) Solutions meeting reliability goal: " + str(reliabilityGoal) + "\n")
        solA = meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, False)
        printSolutions(outputFileA, solA, numOfNodes)
        outputFileA.write(50 * "*" + "\n")
        outputFileA.close()

	# Execute Part B
    solB = None
    if userResponse[1]:
        outputFileB = open("resultPartB.txt", "a")
        outputFileB.write(50 * "*" + "\n")
        outputFileB.write(
            "PART b) Solutions meeting reliability goal: " + str(reliabilityGoal) + " given cost constraint: " + str(
                costGoal) + "\n")
        solB = meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, True)
        printSolutions(outputFileB, solB, numOfNodes)
        outputFileB.write(50 * "*" + "\n")
        outputFileB.close()

    # Execute Part C
    solB = None
    if userResponse[2]:
        if solB is None:
            solB = meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, True)
        outputFileC = open("resultPartC.txt", "a")
        outputFileC.write(50 * "*" + "\n")
        outputFileC.write("PART c) Solution for maximum reliability given cost constraint: " + str(costGoal) + "\n")
        findMaxReliability(outputFileC, solB, numOfNodes)
        outputFileC.write(50 * "*" + "\n")
        outputFileC.close()

if __name__ == "__main__":
    main()