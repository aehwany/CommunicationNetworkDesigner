# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator

try:
	file_path = input("Please set input file path: ")
	reliability_goal = input("Please enter reliability goal: ")
	cost_constraint = input("Please enter cost constraint: ")
except Exception as e:
    print(e)
    exit()
city_list, edge_list = edge_generator.generate(file_path)

print(city_list)
print(edge_list)

