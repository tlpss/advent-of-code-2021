import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import defaultdict

from utils.read_file import read_file
import numpy as np

def split_string(string):
    res = []
    for idx in range(0, len(string)-1):
        # appending sliced string
        res.append(string[idx : idx + 2])
    return res
def insertion_step(start, rules):
    poly_chunks = split_string(start)
    new_poly = ""
    for  i, chunk in enumerate(poly_chunks):
        replace = chunk
        for rule in rules:
            if chunk == rule[0]:
                replace = rule[0][0] + rule [1] + rule[0][1]
                break
        if i == len(start) -2:
            new_poly += replace
        else:
            new_poly += replace[:-1]

    return new_poly
def part1(input_list):
    template, rules = parse_input(input_list)
    print(template, rules)
    poly = template
    for _ in range(10):
        poly = insertion_step(poly, rules)

    calc_(poly)

def calc_(x):
    all_freq = defaultdict(lambda : 0)
    for i in x:
        all_freq[i] += 1
    print(all_freq)
    max_ = max(all_freq.values())
    min_ = min(all_freq.values())
    print(max_ - min_)
    

    
def part2(input_list):
    """
    Too expensive to keep string in memory..

    what determines the sequence? the number of 2-grams of each type (N^2)
    the number of chars is then increased by the inserted element at each step. 

    so bookkeeping of # chars and # n-grams.
    """
    template, rules = parse_input(input_list)
    print(template, rules)
    print(len(rules))
    gram_count =  {rule[0]: 0 for rule in rules}
    rule_dict = {rule[0]: rule[0][0] + rule[1] + rule[0][1] for rule in rules}

    for chunk in split_string(template):
        gram_count[chunk] += 1
    char_count = defaultdict(lambda: 0)
    for c in template:
        char_count[c] += 1

    for i in range(40):
        new_comb_count = gram_count.copy()
        for key,val in gram_count.items():
            new_comb_count[key] -= val
            new_comb_count[rule_dict[key][:-1]] += val
            new_comb_count[rule_dict[key][1:]] += val
            
            char_count[rule_dict[key][1]] += val
        gram_count = new_comb_count
        print(gram_count)

    print(char_count.items())
    print(max(char_count.values()) - min(char_count.values()))
    


def parse_input(input_list):
    template = input_list[0]
    rules = []
    for line in input_list[2:]:
        rules.append(line.split(" -> "))
    return template, rules

if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)