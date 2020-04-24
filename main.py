import edge_generator
import itertools
from edge import Edge

def getTotalCost(list):
    i = 0
    cost = 0
    for i in range(len(list)):
        cost += list[i].cost
    return cost

def getTotalRB(edge, numOfNodes):

    #Find all possible MST
    possibleMST = list(itertools.product([0, 1], repeat = len(edge)))
    i = 0
    while True:
        if i == (len(possibleMST) - 1):
            break 
        elif sum(possibleMST[i]) < numOfNodes-1:
            del possibleMST[i]
        else:
            i += 1
    
    resultRb = 0
    for i in range(len(possibleMST)):
        subGraph = []
        for j in range(len(edge)):
            if possibleMST[i][j] == 1: 
                subGraph.append(edge[j])
                 
        if not checkNodesConnect(subGraph, numOfNodes):
            continue

        sGraphRb = 1
        for j in range(len(possibleMST[0])):
            if possibleMST[i][j] == 1: 
                sGraphRb *= edge[j].reliability
            else:
                 sGraphRb *= (1 - edge[j].reliability)

        resultRb += sGraphRb

    return resultRb

def checkNodesConnect(edge, nodesCount):
    nodesConnected = []
    nodesConnected.append(1)
    i = 0
    while i < nodesCount:
        if len(nodesConnected) <= i:
            return False
        if len(nodesConnected) == nodesCount:
            return True

        for x in range(len(edge)):
            if edge[x].vertice_2 == nodesConnected[i] and edge[x].vertice_1 not in nodesConnected:
                nodesConnected.append(edge[x].vertice_1)

            if edge[x].vertice_1 == nodesConnected[i] and edge[x].vertice_2 not in nodesConnected: 
                nodesConnected.append(edge[x].vertice_2)

        i += 1

def maximizeRb(outputFile, inputG, numOfNodes):
    resultG = []
    MaxReli = 0
    for x in range(len(inputG)):
        if getTotalRB(inputG[x], numOfNodes) > MaxReli:
            resultG = inputG[x]
            MaxReli = getTotalRB(inputG[x], numOfNodes)         
    outputFile.write("\n")

    for x in range(len(resultG)):
        outputFile.write("Edge Number " + str(x+1) + " : " + str(resultG[x].vertice_1) + " - " + str(resultG[x].vertice_2) + " Reliability: " + str(resultG[x].reliability) + " Cost: " + str(resultG[x].cost) + "\n")
    outputFile.write("Total cost: " + str(getTotalCost(resultG)) + "\n")
    outputFile.write("Max Reliability " + str(getTotalRB(resultG,numOfNodes)) + "\n")

def meetGivenReliability(edge, nodesCount, rbGoal, costGoal, constrainedCostBool):
    possibleMST = list(itertools.product([0, 1], repeat = len(edge)))

    resultG = []
    i = 0

    while True:
        if i == (len(possibleMST) - 1):
            break 
        elif sum(possibleMST[i]) < nodesCount-1:
            del possibleMST[i]
        else:
            i += 1

    for i in range(len(possibleMST)):
        graph = []
        for j in range(len(edge)):
            if possibleMST[i][j] == 1: 
                graph.append(edge[j])
                 
        if not checkNodesConnect(graph, nodesCount):
            continue

        if constrainedCostBool and costGoal > 0:
            if getTotalCost(graph) > costGoal:
                continue

        if getTotalRB(graph, nodesCount) >= rbGoal:
            resultG.append(graph)
            
    return resultG

def printSolutions(file,sol, numOfNodes):
    for x in range(len(sol)):
        file.write("Solution No. " + str(x+1) + "\n")
        file.write("Total reliability:" + str(getTotalRB(sol[x], numOfNodes)) + "\n")
        
        for i in range(len(sol[x])):
            file.write("Edge No. " + str(i+1) + ": " + str(sol[x][i].vertice_1) + " - " + str(sol[x][i].vertice_2) + " Reliability: " + str(sol[x][i].reliability) + " Cost: " + str(sol[x][i].cost) + "\n")
        file.write("\n")

def decreasingReli(elem):
    return elem.reliability

def main():
    rbGoal = float(input("Choose reliability goal(Range: 0 to 1): "))
    costGoal = int(input("Choose cost constraint (Range: 1 to 100): "))


    questionA = input("run Question A) Meet given Relability? (y/n) ")
    questionB = input("run QB) max reliability given cost? (y/n) ")

    userResponse = []
    for response in [questionA, questionB]:
        if response == "Y" or response == "y":
            response = True
        else:
            response = False
        userResponse.append(response)

    print("-----"*10)
    print("Reliability goal= " + str(rbGoal))
    print("Cost constraint= " + str(costGoal))
    inputValues = edge_generator.readInputFile(userResponse)
    nodesCount = inputValues[0]
    reliability = inputValues[1]
    cost = inputValues[2]
    edgesCount = inputValues[3]

    edge = [None] * edgesCount
    z = 0
    # Create edge array
    for x in range(nodesCount):
        for y in range(x + 1, nodesCount, 1):
            edge[z] = Edge(x+1, y+1, cost[z], reliability[z])
            z += 1

    #city_list, edge_list = edge_generator2.generate()
    edge.sort(key=decreasingReli, reverse=True)

    # Question A: Meet a given reliability goal
    if userResponse[0]:
        outputFileA = open("qA-Result.txt", "a")
        outputFileA.write("-----" * 10  + "\n")
        outputFileA.write("QA) Results meeting given reliability goal: " + str(rbGoal) + "\n")
        solA = meetGivenReliability(edge, nodesCount, rbGoal, costGoal, False)
        printSolutions(outputFileA, solA, nodesCount)
        outputFileA.write("-----" * 10 + "\n")
        outputFileA.close()

    # Quection B: maximize reiliability subject to given cost constraint
    solB = None
    if userResponse[1]:
        if solB is None:
            solB = meetGivenReliability(edge, nodesCount, rbGoal, costGoal, True)
        outputFileB = open("qB-Result.txt", "a")
        outputFileB.write("-----" * 10 + "\n")
        outputFileB.write("QB) Resuults of maximum reliability subject to given cost constraint: " + str(costGoal) + "\n")
        maximizeRb(outputFileB, solB, nodesCount)
        outputFileB.write("-----" * 10 + "\n")
        outputFileB.close()

if __name__ == "__main__":
    main()