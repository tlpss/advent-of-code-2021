import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def part1(input_list):
    grid = parse_input(input_list)
    
    w = len(grid[0])
    def node_index_to_coord(n):
        return (n//w), n%w
    n_nodes= len(grid) * len(grid[0])

    def get_minimal_distance_not_included_node(distances, included):
        m = 1000000
        for n in range(n_nodes):
            i,j = node_index_to_coord(n)
            if distances[i][j] < m and not included[i][j]:
                m = distances[i][j]
                index = i,j
        return index

    distances = [[1000000 for i in grid[0]] for j in grid]
    distances[0][0] = 0
    included = [[False for i in grid[0]] for j in grid]

    for iter in range(n_nodes):
        i,j = get_minimal_distance_not_included_node(distances, included)
        print(i,j)
        included[i][j] = True
        for shift in [[-1,0], [1,0], [0,1], [0,-1]]:
            i_n, j_n = i + shift[0], j + shift[1]
            if not 0 <= i_n < len(grid) or not 0 <= j_n < len(grid[0]):
                continue
            if not included[i_n][j_n] and distances[i_n][j_n] > distances[i][j] + grid[i_n][j_n]:
                distances[i_n][j_n] = distances[i][j] + grid[i_n][j_n]
    
    print(distances)
    print(distances[-1][-1])

### cannot use DP since one can travel up and left. 
## Dijkstra or A* 
""" 
    dp_cost = [[0 for x in row] for row in grid]
    h,w = len(grid), len(grid[0])

    for i in range(1,w):
        dp_cost[0][i] = dp_cost[0][i-1] + grid[0][i]
    for i in range(1,h):
        dp_cost[i][0] = dp_cost[i-1][0] + grid[i][0]

    for i in range(1, h):
        for j in range(1,w):
            dp_cost[i][j] = min(dp_cost[i-1][j], dp_cost[i][j-1]) + grid[i][j]
    cost = dp_cost[h-1][w-1]
    print(cost)
    return cost
"""
            
    
def part2(input_list):
    grid = parse_input(input_list)
    grid = np.array(grid)
    actual_grid = np.zeros((grid.shape[0] *5, grid.shape[1]*5), dtype = np.uint8)
    w,h = grid.shape
    for i in range(0,5):
        for j in range(0,5):
            g = grid + i + j
            g = np.where (g > 9, g % 9, g)
            print(i,j)
            actual_grid[w*i: w*(i+1), h*j:h*(j+1)] = g
    print(actual_grid)
    

    grid = actual_grid
    w = len(grid[0])
    def node_index_to_coord(n):
        return (n//w), n%w
    n_nodes= len(grid) * len(grid[0])

   
    distances = np.ones_like(grid, dtype=np.uint32) * 100000
    distances[0, 0] = 0
    
    not_included =  np.array([[True for i in grid[0]] for j in grid])
    for iter in range(n_nodes):
        print(iter/n_nodes)
        dst = distances + ( 1 - not_included) * 2000000
        i,j = np.unravel_index(dst.argmin(), dst.shape)
        not_included[i][j] = False
        for shift in [[-1,0], [1,0], [0,1], [0,-1]]:
            i_n, j_n = i + shift[0], j + shift[1]
            if not 0 <= i_n < len(grid) or not 0 <= j_n < len(grid[0]):
                continue
            if  not_included[i_n][j_n] and distances[i_n][j_n] > distances[i][j] + grid[i_n][j_n]:
                distances[i_n][j_n] = distances[i][j] + grid[i_n][j_n]
    
    print(distances)
    print(distances[-1][-1])


def parse_input(input_list):
    grid = [ [int(x) for x in line] for line in input_list]
    return grid
if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)

    part2(input_list)