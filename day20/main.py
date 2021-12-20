import sys
import os
from typing import List 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def apply_filter(padded_image:np.ndarray, filter: List[int]):
    output_image = np.zeros_like(padded_image, dtype= np.int8)
    offsets = [[-1,-1],[-1,0], [-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
    for i in range(1, padded_image.shape[0]-1): 
        for j in range(1, padded_image.shape[1] - 1):
            filter_str = "0b"
            for offset in offsets:
                filter_str+= str(padded_image[i + offset[0],j+ offset[1]])
            
            filter_index = int(filter_str,2)
            value = filter[filter_index]
            output_image[i,j] = value

    
    output_image[0,:] = output_image[1,1]
    output_image[-1,:] = output_image[1,1]
    output_image[:,0] = output_image[1,1]
    output_image[:,-1] = output_image[1,1]


    return output_image

def parse_input(input_list):
    filter_dict = {"#": 1, ".": 0}
    filter = [filter_dict[char] for char in input_list[0]]

    image = []
    for row in input_list[2:]:
        image.append([filter_dict[char] for char in row])
    return np.array(image, dtype=np.int8), filter

"""
padding element (infinite element can either be  0 - 0 - 0 ...; 0 - 1 - 0 - 1 or 0, 1, 1, 1, 1, 1,  depending on the value of filter[0] and filter[9]. 
The case of 1, 1, 1.. leads to an infinite count and hence does not occur in the input
the other cases result in a zero padding element for even iterations (2,50) 

The image grows with size 1 at each iteration.
-> simply pad image with # iterations + 1 at each side.
"""
def part1(input_list):
    image, filter = parse_input(input_list)
    size = image.shape
    padded_image = np.zeros((size[0] + 8, size[1] + 8), dtype=np.int8)
    padded_image[4:-4, 4: -4] = image
    print(filter)
    print(padded_image)
    image = apply_filter(padded_image,filter)
    print(image)
    image = apply_filter(image, filter)
    print(image)
    print(np.sum(image)) 

    
def part2(input_list, iterations):
    image, filter = parse_input(input_list)
    size = image.shape
    padded_image = np.zeros((size[0] + iterations*2 + 2, size[1] + iterations*2 +2), dtype=np.int8)
    padded_image[iterations +1:-iterations - 1, iterations +1:- iterations -1] = image
    img = padded_image
    for i in range(iterations):
        img = apply_filter(img, filter)
        print(img)
    print(np.sum(img))


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    part1(input_list)
    part2(input_list, 50)

    