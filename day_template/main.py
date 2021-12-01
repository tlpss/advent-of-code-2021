import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def part1(input_list):
    pass
    
def part2(input_list):
    pass


if __name__ == "__main__":
    line_list = read_file(    path = os.path.join(sys.path[0], "input.txt"))
    input_list = [int(item) for item in line_list]
    test_list = []
    #part1(input_list)
    #part2(input_list)