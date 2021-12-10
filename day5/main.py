import sys
import os
from typing import List, NamedTuple 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np
from dataclasses import dataclass
import math 
class GridPoint(NamedTuple):
    x: int
    y: int


@dataclass
class HydroVentLine:
    start: GridPoint
    end: GridPoint

    def is_horizontal(self):
        return self.start.y == self.end.y
    
    def is_vertical(self):
        return self.start.x == self.end.x
    
    def is_diagonal(self):
        if self.is_horizontal():
            return False
        if self.is_vertical():
            return False
        return True
    
    def max_coordinate(self):
        return max(self.start.x, self.start.y, self.end.x, self.end.y)

class HydroVentMap:
    def __init__(self):

        self.dim = 6
        self.map = np.zeros((self.dim, self.dim),dtype=np.int8)

    def _update_map(self, line: HydroVentLine, diagonal: bool = False):

        # update grid size of required:
        if line.max_coordinate() +1  > self.dim:
            new_dim = line.max_coordinate() + 1 
            new_map = np.zeros((new_dim,new_dim), dtype=np.int8)
            new_map[:self.dim, :self.dim] = self.map
            self.map = new_map
            self.dim = new_dim

        # add line to grid
        print(line)
        if line.is_diagonal():
            if diagonal is True:

                x_range = np.absolute(line.end.x - line.start.x)
                if line.end.x < line.start.x:
                    x_step = -1 
                else: 
                    x_step = 1

                y_range = np.absolute(line.end.y - line.start.y)
                if line.end.y < line.start.y:
                    y_step = -1
                else:
                    y_step = 1

                for i in range(np.absolute(line.end.x-line.start.x) +1 ):
                    x = line.start.x + i * x_step
                    y = line.start.y + i * y_step
                    print(f"{x},{y}")
                    self.map[x,y] += 1
                
        if line.is_horizontal():
            x_start = min(line.start.x, line.end.x)
            x_end = max(line.start.x, line.end.x) +1 
            self.map[x_start: x_end, line.start.y] += 1

        if line.is_vertical():
            y_start = min(line.start.y, line.end.y)
            y_end = max(line.start.y, line.end.y) +1 
            self.map[line.start.x, y_start:y_end] += 1
        print(self.map)
        #print(self.map)
        

    def get_amount_of_overlapping_cells(self):
        indices = np.where(self.map >1)
        return len(indices[0])

def parse_input(input_list: List[str]) -> List[HydroVentLine]:
    list_of_lines = []
    for line in input_list:
        inputs = [int(x) for x in line.replace(" -> ", ",").split(",")]
        list_of_lines.append(
            HydroVentLine(
                GridPoint(inputs[0], inputs[1]), 
                GridPoint(inputs[2], inputs[3])
                )
            )
    return list_of_lines

def part1(input_list):
    lines = parse_input(input_list)

    grid = HydroVentMap()    
    for line in lines:
        grid._update_map(line)

    print(grid.get_amount_of_overlapping_cells())
def part2(input_list):
    lines = parse_input(input_list)

    grid = HydroVentMap()    
    for line in lines:
        grid._update_map(line, diagonal=True)
    print(grid.get_amount_of_overlapping_cells())
    

if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)