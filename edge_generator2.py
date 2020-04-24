import string
from edge import Edge
alphabet_list = list(string.ascii_uppercase)


def readInputFile(answer_list):
    lines = [line for line in open('input.txt') if not line.startswith('#') and
             len(line.strip())]
    numOfNodes = int(lines[0].split("\n")[0])
    reliability = list(map(float, lines[1].split("\n")[0].split(" ")))
    cost = list(map(float, lines[2].split("\n")[0].split(" ")))
    edgeNum = len(reliability)

    print("Number of Nodes:", numOfNodes)
    print("Reliability Matrix:" , reliability)
    print("Cost Matrix:" , cost)
    print("Number of edges:", edgeNum)

    if answer_list[0]:
        runPart("resultPartA.txt",numOfNodes, reliability,cost, edgeNum)
        print("running A")

    if answer_list[1]:
        runPart("resultPartB.txt",numOfNodes, reliability,cost, edgeNum)
        print("running B")

    if answer_list[2]:
        runPart("resultPartC.txt",numOfNodes, reliability,cost, edgeNum)
        print("running C")

    return [numOfNodes, reliability, cost, edgeNum]

def read_data(filePath):
    number_of_cities = None
    costs = None
    reliabilities = None
    input_file = open(filePath)
    for line in input_file:
        if '#' in line:
            continue
        if number_of_cities is None:
            number_of_cities = line
            continue
        if reliabilities is None:
            reliabilities = line.rstrip('\n').split(' ')
            continue
        if costs is None:
            costs = line.rstrip('\n').split(' ')
            continue
    return number_of_cities,costs,reliabilities


def generate():
    number_of_cities, costs,reliabilities = read_data("input.txt")
    city_list = alphabet_list[0:int(number_of_cities)]
    edge_list = list()
    row = 0
    col = 1

    for reliability,cost in zip(reliabilities,costs):
        edge_list.append(Edge(city_list[row],city_list[col],float(cost),float(reliability)))
        if(col == len(city_list)-1):
            row = row+1
            col = row+1
        else:
            col= col+1
    return city_list, edge_list


def runPart(file, numOfNodes, reliability,cost, edgeNum):
    outputFile = open(file, "w")
    outputFile.write("Number of Nodes: " + str(numOfNodes) + "\n")
    outputFile.write("Reliability Matrix: " + str(reliability) + "\n")
    outputFile.write("Cost Matrix: " + str(cost) + "\n")
    outputFile.write("Number of edges: " + str(edgeNum) + "\n")
    outputFile.close()