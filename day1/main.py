import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)
from utils.read_file import read_file
import numpy as np

def part1(input_list):
    np_input = np.array(input_list)

    result = np_input[:-1] < np_input[1:]
    print(result)
    result = sum(result)
    print(result)
    
def part2(input_list):

    list_3 = []
    for i in range(len(input_list)-2):
        list_3.append(input_list[i] + input_list[i+1] + input_list[i+2])
    print(list_3)

    np_list_3 = np.array(list_3)

    result = np_list_3[:-1] < np_list_3[1:]
    print(result)
    print(sum(result))


if __name__ == "__main__":
    line_list = read_file(    path = os.path.join(sys.path[0], "input.txt"))
    input_list = [int(item) for item in line_list]
    test_list = [199,200,208,210,200,207,240,269,260,263]
    #part1()
    part2(input_list)

    