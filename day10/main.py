from collections import defaultdict
import sys
import os
from typing import Union 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def find_first_illegal_character(seq: str) -> Union[str, None]:
    open_syntax = "({[<"

    open_count = {'(': 0, '[': 0, '{' : 0, '<': 0}
    open_to_close_dict = {'(': ')', '[': ']', '{': '}', '<' :'>'}
    close_top_open_dict = {v:k for k,v in open_to_close_dict.items()}
    
    chunk_list = []
    for s in seq:
        if s in open_syntax:
            chunk_list.append(s)
        else:
            if chunk_list[-1] != close_top_open_dict[s]:
                return s
            else:
                chunk_list = chunk_list[:-1]
    return None
        

def part1(input_list):
    first_illegal_chars = []
    for line in input_list:
        first_illegal_chars.append(find_first_illegal_character(line))
    
    score_dict =dict( {")": 3, "]": 57, "}": 1197, ">": 25137})

    score = 0
    for item in first_illegal_chars:
            score += score_dict.get(item, 0)
    print(score)

def complete_line(seq: str):
    open_syntax = "({[<"

    open_count = {'(': 0, '[': 0, '{' : 0, '<': 0}
    open_to_close_dict = {'(': ')', '[': ']', '{': '}', '<' :'>'}
    close_top_open_dict = {v:k for k,v in open_to_close_dict.items()}
    
    chunk_list = []
    for s in seq:
        if s in open_syntax:
            chunk_list.append(s)
        else:
            chunk_list = chunk_list[:-1]
    
    # complete:
    s = ""
    for open in chunk_list[::-1]:
        s += open_to_close_dict[open]

    return s

def incomplete_score(s: str):
    score_dict =dict( {")": 1, "]": 2, "}": 3, ">": 4})
    score = 0
    for char in s:
        score*=5
        score += score_dict[char]
    return score

def part2(input_list):

    incomplete_seq_scores = []
    for line in input_list:
        if not find_first_illegal_character(line):
            s = complete_line(line)
            incomplete_seq_scores.append(incomplete_score(s))
        
    score = sorted(incomplete_seq_scores)
    print(score)
    index = len(score)//2
    print(index)
    score = score[index]
    print(score)
    

    


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)