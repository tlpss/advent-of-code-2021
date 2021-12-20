import sys
import os
from typing import List 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

def part1(input_list):
    pass
    
def part2(input_list):
    # slow to run part1...
    # so take TF values from cmd and do manhattan distance myself.
    tfs = [ 
        [  -34,   -39, -1212],
        [ 1276,   -97, -1275],
        [ -23,  -18, 1148],
        [ -16,   29, 2262],
        [-1232,    18, -1286],
        [-2296,   -97, -1318],
        [-1152,  1250, -1236],
        [-2361,    82, -2400],
        [-2394,    32, -3766],
        [-1185,   -91, -2525],
        [-2457,   -48, -4796],
        [-2413, -1237, -3623],
        [-2354,  1125, -3678],
        [-2424, -1251, -1267],
        [-1164, -1250,    15],
        [-3490, -1240, -1188],
        [-2426,  1264, -2514],
        [-2341,  1264, -1211],
        [-2307, -2338, -1261],
        [-2316, -2427,     3],
        [-3651, -2454,    15],
        [-3533, -3667,  -159],
        [-3623,     9, -3737],
        [-3477,  1147, -2567],
        [-2306, -1164,    24]
    ]

    max_d = 0
    for i in range(25):
        for j in range(25):
            d = sum([abs(tfs[i][k] - tfs[j][k]) for k in range(3)])
            if d > max_d:
                max_d = d
    print(max_d)
def generate_orientations(array):
    array_orientations = []
    for permutation in range(3): # select which axis to consider as "front"
        for flip in [0,1]: # select oriention on axis
            for rot2d in [np.array([[1,0],[0,1]]), np.array([[0,-1],[1,0]]), np.array([[-1,0],[0,-1]]),np.array([[0,1],[-1,0]]) ]: # select top orientation of remaining 2D plane
                arr = np.copy(array)
                arr = np.roll(arr, permutation, axis=1)
                if flip:
                    arr[:,0] *= -1
                    arr[:,2] *= -1                

                arr[:,1:] = arr[:,1:] @ rot2d

                array_orientations.append([arr, (permutation,flip, rot2d)])
    return array_orientations

def count_overlapping(pc1,pc2):
    a1 = pc1.tolist()
    a2 = pc2.tolist()
    counter = 0
    for point in a1:
        if point in a2:
            counter += 1
    return counter

def get_transform_1_to_2(pc1, pc2, count = 12):
    pc1 = np.copy(pc1)
    pc2 = np.copy(pc2)

    for p1 in pc1:
        pc1_local = pc1 - p1
        for p2 in pc2:
            pc2_local = pc2 - p2
            counter = count_overlapping(pc1_local, pc2_local)
            if counter >= 12:
                return p1 - p2, counter
    
    return None, None

def match_clouds(pc1,pc2,count =12):
    for cloud, orientation in generate_orientations(pc2):
        tf, count= get_transform_1_to_2(pc1,cloud,count)
        if tf is not None:
            return tf, orientation, cloud
    return None, None, None

def parse_input(input_list):
    sensor_arr = []
    while(len(input_list)> 0):
        input_list = input_list[2:]
        arr = []
        while( len(input_list) > 0 and input_list[0][:1] != ""):
            arr.append([int(x) for x in input_list[0].split(",")])
            input_list = input_list[1:]
        sensor_arr.append(arr)
    
    return sensor_arr

def match(list_of_clouds: List):
    beacons = set()
    pc1 = list_of_clouds.pop(0)
    for beacon in pc1:
        beacons.add(tuple(beacon.tolist()))

    while(len(list_of_clouds) >= 1):
        for i, pc2 in enumerate(list_of_clouds):
            tf, orientation, cloud = match_clouds(pc1, pc2)
            print(tf)
            if tf is not None:
                print("match")
                print(tf)
                print(orientation)
                pc2_global = cloud + tf
                print(pc2)
                list_of_clouds = [list_of_clouds[j] for j in range(len(list_of_clouds)) if i != j]
                for beacon in pc2_global:
                    beacons.add(tuple(beacon.tolist()))
                pc1 = np.array([list(x) for x in beacons])
                break
    return beacons

if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    #part2(input_list)
    sensor_list = parse_input(input_list)

    sensor_list = [np.array(x) for x in sensor_list]
    # v = get_transform_1_to_2(sensor_list[0],sensor_list[1],3)
    # print(v)

    #print(match_clouds(sensor_list[3], sensor_list[1],12))
    # b = match(sensor_list)
    # print(b)
    # print(len(b))
    part2("")
