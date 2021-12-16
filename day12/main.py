from collections import defaultdict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def construct_graph_dict(input_list):
    graph = defaultdict(list)
    for connection in input_list:
        a,b = connection.split("-")
        graph[a].append(b)
        graph[b].append(a)
    return graph
        

def part1(input_list):
    graph = construct_graph_dict(input_list)
    
    queue = [["start"]]
    complete_paths = []

    while len(queue) > 0:
        path = queue.pop(0)
        if path[-1] == "end":
            complete_paths.append(path)
        else:
            for nb in graph[path[-1]]:
                nb : str
                if not (nb.islower() and nb in path):   
                    p = path.copy()
                    p.append(nb)
                    queue.append(p)
    print(complete_paths)
    print(len(complete_paths))
    return complete_paths

def is_valid_path(path: list):
    duplicate = None
    for node in path:
        if node =="end":
            if path.count("end") > 1:
                return False
        if node =="start":
            if path.count("start") > 1:
                return False
        if node.islower():
            if path.count(node) == 2:
                if duplicate is None:
                    duplicate = node
                else:
                    if node != duplicate:
                        return False

            if path.count(node) > 2:
                return False
    return True
def part2(input_list):
    graph = construct_graph_dict(input_list)
    
    queue = [["start"]]
    complete_paths = []

    while len(queue) > 0:
        path = queue.pop(0)
        if path[-1] == "end":
            complete_paths.append(path)
        else:
            for nb in graph[path[-1]]:
                nb : str
                p = path.copy()
                p.append(nb)
                if (is_valid_path(p)):
                    queue.append(p)
    print(len(complete_paths))
    return complete_paths


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)