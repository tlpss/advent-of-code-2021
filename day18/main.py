from __future__ import annotations

import sys
import os
from typing import Union 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

from dataclasses import dataclass
import math

 #@dataclass(unsafe_hash=True) # weird error due to __eq__ not using a hash...
class SnailNumber:
    def __init__(self, x,y,val, parent = None) -> None:
        self.x  =x 
        self.y = y
        self.val = val
        self.parent = parent


    @classmethod
    def list_to_snail_tree(cls,l, parent = None):

        if isinstance(l, int):
            return SnailNumber(None,None, l, parent)
        else:
            assert isinstance(l, list)
            s = SnailNumber(None,None,None,parent)
            s.x = SnailNumber.list_to_snail_tree(l[0], parent = s)
            s.y = SnailNumber.list_to_snail_tree(l[1], parent = s)
    
            return s
        
    def to_list(self):
        if self.val != None:
            return self.val
        
        else:
            return [self.x.to_list(), self.y.to_list()]
        

    def snail_magnitude(self):
        if self.val is not None:
            return self.val
        else:
            return 3 * self.x.snail_magnitude()+ 2 * self.y.snail_magnitude()
        


def add(number1, number2, reducer):
    number = SnailNumber(number1, number2,None,None)
    number1.parent = number
    number2.parent = number
    changed = True
    while(changed):
        number, changed  = reducer.reduce_round(number)

    return number

class NumberReduction:
    def __init__(self) -> None:
        self.splitted = False
        self.exploded = False
        self.exploded_node = None
    def reduce_round(self,number):
        number = self.explode(number, new_explode =  True)
        if self.exploded:
            return number, True
        else:
            number = self.split(number, new_split= True)
            return number, self.splitted

    def explode(self, snail: SnailNumber, depth = 0, new_explode = False):
        if new_explode:
            self.exploded = False

        if snail.val is not None:
            return snail
        if depth >= 4 and snail.x.val is not None and snail.y.val is not None and not self.exploded:
            self.exploded = True
            left_val = snail.x.val
            right_val = snail.y.val
            snail.x = None
            snail.y = None
            snail.val = 0
            self.add_left(snail, left_val)
            self.add_right(snail, right_val)
            return snail 

        snail.x = self.explode(snail.x, depth = depth + 1)
        snail.y = self.explode(snail.y, depth = depth +1) 
        return snail
        
    def add_right(self,snail,val):
        while snail.parent is not None:
            if snail == snail.parent.x:
                y = snail.parent.y 
                while y.x != None:
                    y = y.x

                y.val += val
                return 
            snail = snail.parent

    def add_left(self,snail,val):
        while snail.parent is not None:
            if snail == snail.parent.y:
                y = snail.parent.x
                while y.y is not None:
                    y = y.y
                y.val += val
                return 
            snail = snail.parent

    
    def split(self, snail, new_split = False):
        if new_split:
            self.splitted = False
        
        if snail.val is not None:
            if snail.val >=10 and not self.splitted:
                self.splitted = True
                
                snail.x = SnailNumber(None, None, math.floor(snail.val /2),snail)
                snail.y = SnailNumber(None,None,math.ceil(snail.val /2), snail)
                snail.val = None
            return snail 

        self.split(snail.x)
        self.split(snail.y)
        return snail



    
def part1(input_list):
    reducer = NumberReduction()
    n = SnailNumber.list_to_snail_tree(eval(input_list[0]))
    for row in input_list[1:]:
        n = add(n, SnailNumber.list_to_snail_tree(eval(row)),reducer)
    print(n.snail_magnitude())
    
def part2(input_list):
    max_mag = 0
    for row1 in input_list:
        for row2 in input_list:
            if row1 == row2:
                continue

            n1 = SnailNumber.list_to_snail_tree(eval(row1))
            n2 = SnailNumber.list_to_snail_tree(eval(row2))
            n = add(n1, n2, NumberReduction())
            mag = n.snail_magnitude()
            if mag > max_mag:
                print("°°---22SZEZEMLZKJEF")
                print(row1)
                print(row2)
                print(mag)
                max_mag = mag
            #### numbers are changed in place... bad design... 
            # solution: just create them again from the immutable string

            ### STUPID n1 + n2 is enough!! since i'm going over all rows and cols... 
            
    print(max_mag)
    return max_mag



if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list)
    #part2(input_list)
    # r = NumberReduction()
    # n = SnailNumber.list_to_snail_tree([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    # print(n.to_list())
    # n = r.explode(n,new_explode=True)
    # print(n.to_list())
    # print(n)
    # n = r.split(n, True)
    # print(n)
    # n = SnailNumber.list_to_snail_tree([[[[[9,8],1],2],3],4])
    # print(n.to_list())
    # n = r.explode(n, new_explode=True)
    # print(n.to_list())
    # n = SnailNumber.list_to_snail_tree([7,[6,[5,[4,[3,2]]]]])
    # print(n.to_list())
    # n = r.explode(n, new_explode=True)
    # print(n.to_list())
    # n = SnailNumber.list_to_snail_tree([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    # print(n.to_list())
    # n = r.explode(n, new_explode=True)
    # print(n.to_list())
    # n = SnailNumber.list_to_snail_tree([[[[0,7],4],[[7,8],[0,13]]],[1,1]])
    # n = NumberReduction().split(n, new_split= True)
    # n = NumberReduction().explode(n, new_explode=True)
    # print(n.to_list())
    # n = SnailNumber.list_to_snail_tree([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])
    # print(n.to_list())
    # print(NumberReduction().explode(n).to_list())

    # n1 = SnailNumber.list_to_snail_tree([[[[4,3],4],4],[7,[[8,4],9]]])
    # n2 = SnailNumber.list_to_snail_tree([1,1])
    # n = add(n1,n2, NumberReduction())
    # print(n.to_list())



    part2(input_list)
