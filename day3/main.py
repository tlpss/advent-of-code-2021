import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def calculate_most_common_string(input_list):
    one_count = [0] * len(input_list[0])
    for bitstring in input_list:
        for j in range(len(bitstring)):
            one_count[j] += int(bitstring[j])
    print(one_count)
    most_common_string = ""
    for j in range(len(input_list[0])):
        threshold = len(input_list)/2

        if one_count[j] >= threshold:
            most_common_string += "1"
        else: 
            most_common_string += "0"
    return most_common_string


def part1(input_list):
    most_common_string = calculate_most_common_string(input_list)
    
    print(most_common_string)
    least_common_string = ''.join('1' if x == '0' else '0' for x in most_common_string)

    gamma = int(most_common_string,2)
    eps = int(least_common_string, 2)
    print(gamma*eps)


def filter_on_most_common(input_list, discard_most = False):
    retain_list: list =  input_list
    
    j = 0
    while(len(retain_list) > 1 and j < len(retain_list[0])):
        most_common_string = calculate_most_common_string(retain_list)
        temp_retain_list = []
        for item in retain_list:
            if item[j] == most_common_string[j] and not discard_most:
                temp_retain_list.append(item)
            if item[j] != most_common_string[j] and discard_most:
                temp_retain_list.append(item)
        retain_list = temp_retain_list
        j+= 1
    retain_list = temp_retain_list
    
    print(retain_list)
    return retain_list[0]

def part2(input_list):
    oxy = filter_on_most_common(input_list, False)
    co2 = filter_on_most_common(input_list, True)
    print(oxy)
    print(co2)

    print( int(oxy, 2) * int(co2, 2))
        



if __name__ == "__main__":
    line_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))

    #part1(line_list)
    part2(line_list)