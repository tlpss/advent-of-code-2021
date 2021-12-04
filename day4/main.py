import sys
import os
from typing import List 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import copy

from utils.read_file import read_file
import numpy as np

class Bingo:
    def __init__(self, board_numbers: List[List[int]]):
        self.size = len(board_numbers)
        self.board_numbers = np.array(board_numbers)
        self.marked_positions = np.zeros_like(self.board_numbers)
        self.last_number_called = None

    def update(self, number: int):
        self.last_number_called = number
        mask = np.where(self.board_numbers == number)
        self.marked_positions[mask] = 1

    def has_won(self) -> bool: 
        row_sums = np.sum(self.marked_positions, axis = 1)
        col_sums = np.sum(self.marked_positions, axis = 0)

        if np.max(row_sums) == 5:
            return True
        if np.max(col_sums) == 5:
            return True
        return False
    def get_score(self) -> int:
        points = np.sum(self.board_numbers[self.marked_positions == 0])
        print(points)
        return points * self.last_number_called
        
def parse_bingo_input(input_list):
    # row 1 = numbers:
    copy_list =copy.deepcopy( input_list)
    copy_list.append("")
    numbers = [ int(v) for v in input_list[0].split(",")]
    boards = []
    temp = []
    for line in copy_list[2:]:
        if line == "":
            print(temp)
            boards.append(Bingo(temp))
            temp = []
        else:
            temp.append([int(v) for v in line.replace("  "," ").split(" ")])
    
    print(numbers)
    print(len(boards))
    return numbers, boards


def part1(input_list):

    
    numbers, boards = parse_bingo_input(input_list)


    for number in numbers:
        for board in boards:
            board.update(number)
            if board.has_won():
                print(board.get_score())
                return
    
def part2(input_list):
        
    numbers, boards = parse_bingo_input(input_list)
    
    for index, number in enumerate(numbers):
        for board in boards:
            board.update(number)
        boards = [board for board in boards if not board.has_won()]
        if len(boards) == 1:
             break

    board = boards[0]
    for number in numbers[index:]:
        board.update(number)
        if board.has_won():
            print(board.get_score())
            return
    

if __name__ == "__main__":
    line_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    parse_bingo_input(test_list)
    #part1(line_list)
    part2(line_list)