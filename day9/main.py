import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

def part1(input_list):
    field = np.array(parse_input(input_list))
    peaks = peak_local_max(10 - field, min_distance = 1, indices  =False, exclude_border = False)
    print(peaks)
    print(np.sum(field[peaks] +1))
    return peaks
def part2(input_list):
    field = np.array(parse_input(input_list))
    peaks = peak_local_max(10 - np.array(field), min_distance = 1, indices  =True, exclude_border = False)

    mask = field != 9

    print(mask)
    print(peaks)
    print(field)

    segmentation = watershed(field, mask = field!=9)
    print(segmentation)

    seg_count  = []
    for i in range(1, np.max(segmentation)+1):
        seg_count.append(np.sum(segmentation == i))
    print(seg_count)

    sorted_seg_count = sorted(seg_count, reverse=True)

    val = sorted_seg_count[0]*sorted_seg_count[1]*sorted_seg_count[2]
    print(val)
def parse_input(input_list):
    return [[int(x) for x in row] for row in input_list]

if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    part2(input_list)