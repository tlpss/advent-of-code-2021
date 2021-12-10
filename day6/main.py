import sys
import os

from numpy.core.fromnumeric import amax 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List

from utils.read_file import read_file
import numpy as np

class Lanternfish:
    def __init__(self, ttr = 8):
        self.time_untill_reproduction = ttr
    
    def update(self):
        if self.time_untill_reproduction == 0:
            self.time_untill_reproduction = 6
            return [self, Lanternfish()]

        else: 
            self.time_untill_reproduction -= 1 
            return [self]
    def __repr__(self):
        return f"{self.time_untill_reproduction}"

def part1(input_list, days = 18): 
    initial_state = parse_input(input_list)
    state = [Lanternfish(x) for x in initial_state]
    for day in range(1, days + 1 ):
        new_state = []
        for fish in state:
            new_state.extend(fish.update())
        print(f"day {day} -> {len(new_state)}")
        state = new_state
        #print(f"day {day} - {state}")
    print(len(state))
    return len(state)



    
def fast(input_list, days = 18):
    initial_state = parse_input(input_list)
    state = np.array(initial_state)
    fishes = {}
    for day in range(1, days+1):
        amount = np.sum(state == 0)
        state = np.concatenate((state, np.array([9] * amount)),axis = 0)
        state[state == 0 ] = 7
        state = state - 1 
        print(f" day {day} -> {len(state)}")
        fishes.update({day:len(state)})
    return fishes

def part2(input_list, days = 18):
    """ first method huge mem / cpu overhead.... ! 
    """
    fish_count = [0] * 9
    initial_state = parse_input(input_list)

    for fish in initial_state:
        fish_count[fish] += 1
    
    for day in range(days):
        new = fish_count[0]
        for i in range(8):
            fish_count[i] = fish_count[i+1]
        fish_count[6] += new
        fish_count[8] = new
        print(sum(fish_count))




def parse_input(input_list) -> List[int]:
    return [int(x) for x in input_list[0].split(",")]
if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list, days= 80)
    part2(input_list, 256)
    #part1(["0"], )






