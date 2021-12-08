import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np


def cost(positions, target:int):
    return int(np.sum(np.absolute(np.array(positions)-target)))
    
def cost2(positions, target:int):
    cost = np.absolute(np.array(positions)-target)
    cost = cost * (cost +1)/2
    return int(np.sum(cost))

def part1(input_list, cost = cost):
    ## cost landscape of this quiz has to be convex
    ## to reduce number of evaluations we can do bracketing..
    ## start with min(list) max(list) and shrink interval based on which of the two is larger.
    positions = parse_input(input_list)
    print(positions)
    left =  min(positions)
    right = max(positions)

    while  left != right:
        print(f"left -> {left}, right -> {right}")
        if cost(positions,left) >= cost(positions,right):
            left = int((left+right)/2) +1 
        else:
            right = int((left+right)/2)
    
    print(left)
    print(cost(positions,left + 1))
    print(f" cost = {cost(positions,left)}")
    print(cost(positions, left -1))


def part2(input_list):
    return part1(input_list, cost2)

def parse_input(input_list):
    return [int(x) for x in input_list[0].split(",")]
if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)
    