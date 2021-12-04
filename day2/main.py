import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def part1(input_list):
    hor_pos = 0
    depth = 0
    for command in input_list:
        if command[0] == "forward":
            hor_pos += int(command[1])
        elif command[0] == "down":
            depth += int(command[1])
        else:
            depth -= int(command[1])

    print(hor_pos)
    print(depth)
    print(hor_pos * depth)
    
def part2(input_list):
    hor_pos = 0
    depth = 0
    aim = 0
    for command in input_list:
        if command[0] == "forward":
            hor_pos += int(command[1])
            depth += int(command[1]) * aim
        elif command[0] == "down":
            aim += int(command[1])
        else:
            aim -= int(command[1])

    print(hor_pos)
    print(depth)
    print(hor_pos * depth)


if __name__ == "__main__":
    line_list = read_file(    path = os.path.join(sys.path[0], "input.txt"))
    input_list = [ v.split(" ") for v in line_list]
    #print(input_list)
    #part1(input_list)
    part2(input_list)