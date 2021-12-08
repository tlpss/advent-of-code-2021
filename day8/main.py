import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def part1(input_list):
    amount = 0
    input_list = parse_input(input_list)
    for display in input_list:
        patterns = display[0]
        outputs = display[1]

        digits = [None] * 9

        digits[1] = get_strings_of_length(patterns, 2)[0]
        digits[4] = get_strings_of_length(patterns, 4)[0]
        digits[7] = get_strings_of_length(patterns, 3)[0]
        digits[8] = get_strings_of_length(patterns, 7)[0]
        

        for digit in outputs:
            if digit in digits:
                amount +=1 
    print(amount)


def get_strings_of_length(input_list, length):
    return [x for x in input_list if len(x) == length]
def shared_chars(str1: str, str2:str):
    amount  = 0
    for char in str1:
        amount += str2.count(char)
    return amount

def part2(input_list):
    input_list = parse_input(input_list)
    amount = 0
    for display in input_list:
        patterns = display[0]
        outputs = display[1]

        digits = [None] * 10

        digits[1] = get_strings_of_length(patterns, 2)[0]
        digits[4] = get_strings_of_length(patterns, 4)[0]
        digits[7] = get_strings_of_length(patterns, 3)[0]
        digits[8] = get_strings_of_length(patterns, 7)[0]
        
        filter = [x for x in get_strings_of_length(patterns, 6) if shared_chars( digits[4], x) == 4]
        digits[9] = filter[0]
        digits[0] = [ x for x in get_strings_of_length(patterns, 6) if shared_chars( digits[1], x) == 2 and shared_chars(digits[9],x) != 6][0]
        digits[6] = [ x for x in get_strings_of_length(patterns, 6) if x is not digits[0] and x is not digits[9]][0]
 
        digits[3] = [ x for x in get_strings_of_length(patterns, 5) if shared_chars(digits[1],x) == 2][0]
        digits[2] = [ x for x in get_strings_of_length(patterns, 5) if shared_chars(x, digits[4]) == 2][0]
        digits[5] = [ x for x in get_strings_of_length(patterns, 5) if shared_chars(x, digits[4]) == 3 and x is not digits[3]][0]
        print(digits)
        value  =  0
        for i in range(4):
            print(outputs[i])
            value += digits.index(outputs[i])* 10**(3-i)
        amount += value
    print(amount)

def parse_input(input_list):
    parsed = []
    for row in input_list:
        p  = row.split("|")
        parsed.append([["".join(sorted(x ))for x in p[0].split(" ") if x is not ""], ["".join(sorted(x )) for x in p[1].split(" ") if x is not ""]])
    return parsed 

if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    parse_input(test_list)
    #part1(input_list)
    part2(input_list)