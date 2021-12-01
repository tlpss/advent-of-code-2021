from typing import  List
import os
import sys

def read_file(path: str) -> List[str]:
    line_list = []
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            line_list.append(line.strip())
    return line_list