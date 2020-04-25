import itertools
import string

class NetworkSolver(object):
    def __init__(self, edge_list, number_of_cities, reliability_goal, cost_budget):
        self.edge_list = edge_list
        self.number_of_cities = number_of_cities
        self.reliability_goal = reliability_goal
        self.cost_budget = cost_budget

    def __repr__(self):
        return 'edge_list: {}, number_of_cities: {}, reliability_goal: {}, : cost_budget: {} \n'.format(self.edge_list,
                                                                    self.number_of_cities,
                                                                    self.reliability_goal,
                                                                    self.cost_budget)

    def meets_cost_constraint(self):
        if self.cost_budget==0:
            return []
        potentialMSTs = list(itertools.product([0, 1], repeat=len(self.edge_list)))
        acceptedSet = []
        i = 0
        while True:
            if i == (len(potentialMSTs) - 1):
                break
            elif sum(potentialMSTs[i]) < self.number_of_cities - 1:
                del potentialMSTs[i]
            else:
                i += 1

        for edges in potentialMSTs:
            graph = []
            for j in range(len(self.edge_list)):
                if edges[j] == 1:
                    graph.append(self.edge_list[j])

            if not NetworkSolver.is_connected(graph, self.number_of_cities):
                continue

            if self.cost_budget > 0:
                if NetworkSolver.get_total_cost(graph) > self.cost_budget:
                    continue

            acceptedSet.append(graph)
        return acceptedSet

    @staticmethod
    def is_connected(graph, number_of_cities):
        if len(graph) < 1:
            return False

        # Construct adjacency
        adj = {}
        for edge in graph:
            if edge.vertice_1 not in adj:
                adj[edge.vertice_1] = [edge.vertice_2]
            else:
                adj[edge.vertice_1].append(edge.vertice_2)

            if edge.vertice_2 not in adj:
                adj[edge.vertice_2] = [edge.vertice_1]
            else:
                adj[edge.vertice_2].append(edge.vertice_1)

        # Keep track of visited
        visited = {v:0 for v in list(string.ascii_uppercase)[0:number_of_cities]}

        # DFS
        stack = list()
        stack.append(graph[0].vertice_1)

        while len(stack):
            s = stack[-1]
            stack.pop()

            visited[s] = 1
            for neighbour in adj[s]:
                if not visited[neighbour] == 1:
                    stack.append(neighbour)

        if sum([v for (k,v) in visited.items()]) != number_of_cities:
            return False
        else:
            return True

    @staticmethod
    def get_total_cost(graph):
        i = 0
        cost = 0
        for edge in graph:
            cost += edge.getCost()
        return cost

    @staticmethod
    def get_total_reliability(graph, number_of_cities):
        # Find all possible MST
        combinations = list(itertools.product([0, 1], repeat=len(graph)))
        i = 0
        while True:
            if i == (len(combinations) - 1):
                break
            else:
                i += 1

        resultRb = 0
        for edges in combinations:
            subGraph = []
            for i in range(len(graph)):
                if edges[i] == 1:
                    subGraph.append(graph[i])

            if not NetworkSolver.is_connected(subGraph, number_of_cities):
                continue
            sGraphRb = 1
            for j in range(len(combinations[0])):
                if edges[j] == 1:
                    sGraphRb *= graph[j].reliability
                else:
                    sGraphRb *= (1 - graph[j].reliability)
            resultRb += sGraphRb
        return resultRb

    @staticmethod
    def find_max_reliability(solutions, number_of_cities):
        max_reliability_graph = None
        max_reliability = 0
        for graph in solutions:
            reliability = NetworkSolver.get_total_reliability(graph, number_of_cities)
            if reliability > max_reliability:
                max_reliability_graph = graph
                max_reliability = reliability
        return max_reliability, max_reliability_graph
