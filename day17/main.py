import sys
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np
import math

def part1(xmin, xmax, ymin, ymax):
    # want to take as much steps before reaching final x
    # so slowest speed
    vx = math.floor(-1/2 + math.sqrt(2*xmax))
    print(vx)

    vy = 0
    for _ in range(127):
        print(vy)
        simulate_trajectory(vx,vy,xmin,xmax,ymin, ymax)
        vy += 1 
def part2(xmin, xmax, ymin, ymax):
    vx_max =  math.floor(-1/2 + math.sqrt(2*xmax))
    count = 0
    for vx in range(1000):
        print(f"vx={vx}")
        for vy in range(-1000,1000):
            if simulate_trajectory2(vx,vy,xmin,xmax,ymin,ymax):
                count += 1
    print(count)

def simulate_trajectory(v_x,v_y, xmin, xmax, ymin, ymax):
    time = 0
    x,y  =0,0
    vx,vy = v_x, v_y
    while x + vx <= xmax and y + vy>= ymin:
        x += vx
        y += vy
        vx = vx -1 if vx > 0 else 0
        vy = vy -1
        #print(x,y)
    if (xmin <= x and x <= xmax and ymin <= y and y <= ymax):
        print(f"{v_y} valid!")
    else:
        print("not valid")

def simulate_trajectory2(v_x,v_y, xmin, xmax, ymin, ymax):
    time = 0
    x,y  =0,0
    vx,vy = v_x, v_y
    while x + vx <= xmax and y + vy>= ymin:
        x += vx
        y += vy
        vx = vx -1 if vx > 0 else 0
        vy = vy -1
        #print(x,y)
    if (xmin <= x and x <= xmax and ymin <= y and y <= ymax):
        print(v_x,v_y)
        return True
    else:
        return False


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(20,30,-10, -5)
    #part1(217, 240, -126, -69)
    #part2(20,30,-10,-5)
    part2(217, 240, -126, -69)
