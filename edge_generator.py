import string
from edge import Edge
alphabet_list = list(string.ascii_uppercase)


def readInputFile(userResponse):
    lines = [line for line in open('input.txt') if not line.startswith('#') and
             len(line.strip())]
    nodesCount = int(lines[0].split("\n")[0])
    reliability = list(map(float, lines[1].split("\n")[0].split(" ")))
    cost = list(map(float, lines[2].split("\n")[0].split(" ")))
    edgesCount = len(reliability)

    print("Number of Nodes:", nodesCount)
    print("Reliability Matrix:" , reliability)
    print("Cost Matrix:" , cost)
    print("Number of edges:", edgesCount)

    if userResponse[0]:
        writeFile("resultPartA.txt",nodesCount, reliability,cost, edgesCount)
        print("running A")

    if userResponse[1]:
        writeFile("resultPartB.txt",nodesCount, reliability,cost, edgesCount)
        print("running B")

    return [nodesCount, reliability, cost, edgesCount]

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


def writeFile(file, nodesCount, reliability,cost, edgesCount):
    outputFile = open(file, "w")
    outputFile.write("Number of Nodes: " + str(nodesCount) + "\n")
    outputFile.write("Reliability Matrix: " + str(reliability) + "\n")
    outputFile.write("Cost Matrix: " + str(cost) + "\n")
    outputFile.write("Number of edges: " + str(edgesCount) + "\n")
    outputFile.close()