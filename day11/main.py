import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.read_file import read_file
import numpy as np

class OctoGrid:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.n_glowed = 0
    def step(self):
        #update energy
        self.grid +=1 

        #glow sequence
        not_glowed_grid = np.ones_like(self.grid)
        glow_queue = []
        glow_queue.extend(np.argwhere(self.grid == 10))
        while(len(glow_queue) != 0):
            glow_idx = glow_queue.pop(0)
            if not_glowed_grid[glow_idx[0],glow_idx[1]] == 0:
                continue
            
            self.n_glowed += 1 
            not_glowed_grid[glow_idx[0],glow_idx[1]] = 0
            m = self._get_mask(glow_idx)
            self.grid[m==1] +=1
            glowers = np.argwhere(self.grid * not_glowed_grid == 10)
            glow_queue.extend(glowers)
        
        # cleanup
        self.grid[self.grid > 9] = 0

    def simulate(self,steps):
        for step in range(1,steps+1):
            self.step()
            if np.max(self.grid) == 0:
                print("simultaneous flash")
                print(step)
                print(self.grid)
                break
        print(f"{self.n_glowed=}")



    def _get_mask(self,coord):
        dim = self.grid.shape[0] + 2
        mask = np.zeros((dim,dim), dtype=np.uint8)
        mask[coord[0]:coord[0]+3, coord[1]:coord[1]+3] = 1
        return mask[1:-1,1:-1]
        

def part1(input_list,steps):
    grid = np.array(parse_input(input_list))
    grid = OctoGrid(grid)
    grid.simulate(steps)
    
def part2(input_list):
        grid = np.array(parse_input(input_list))
        grid = OctoGrid(grid)
        grid.simulate(1000)

def parse_input(input_list):
    return [[int(x) for x in row] for row in input_list]


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list, 100)
    part2(input_list)