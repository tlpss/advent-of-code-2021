import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np


def mirror(x, axis):
    if x < axis:
        return x
    else:
        return -(x-axis) + axis

    
def handle_instruction(coords, instruction):
    axis, index = instruction
    new_coords = set()
    for coord in coords:
        x,y = coord
        if axis == "x":
            x = mirror(x, index)
        else:
            y = mirror(y, index)
        new_coord = (x,y)
        new_coords.add(new_coord)
    return new_coords
def part1(input_list):
    coord_list, instructions = parse_input(input_list)
    coords = set()
    for coord in coord_list:
        coords.add(coord)
    print(coords)
    coords = handle_instruction(coords, instructions[0])
    print(coords)
    print(len(coords))
    
def part2(input_list):
    coord_list, instructions = parse_input(input_list)
    coords = set()
    for coord in coord_list:
        coords.add(coord)
    for instruction in instructions:
        coords = handle_instruction(coords, instruction)
    output_code(coords)

    

def output_code(coords):
    dim = (40,40)
    grid = np.zeros(dim, dtype= np.uint8)
    for coord in coords:
        grid[coord[1],coord[0]] = 1
    print(grid)
    np.savetxt("grid.txt", grid, fmt = "%1d")


def parse_input(input_list):
    coords = []
    instructions = []

    positions = True
    for line in input_list:
        if line == "":
            positions = False
            continue
        if positions:
            coords.append(tuple([int(x) for x in line.split(",")]))
        else:
            instruction = line.split(' ')[-1].split("=")
            instruction[-1] = int(instruction[-1])
            instructions.append(instruction)
    return coords, instructions

if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)