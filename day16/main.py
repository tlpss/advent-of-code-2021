import sys
import os
from typing import Dict, List, Tuple, Union, no_type_check 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.read_file import read_file
import numpy as np

from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Packet:
    version: int
    type: int
    bit_len: int 


@dataclass(unsafe_hash=True)
class OperatorPacket(Packet):
    len_type: int
    n_subpackats: int
    n_subbits: int

@dataclass(unsafe_hash=True)
class LiteralPacket(Packet):
    Literalvalue: int

def to_int(bitstring):
    return int(bitstring, 2)

def get_and_split(bitstring, x):
    return bitstring[:x], bitstring[x:]
class PacketDecoder:
    @classmethod
    def decode_packet(cls, bitstring: str) -> Tuple[Packet, str]:
        
        version, bitstring = get_and_split(bitstring, 3)
        version = to_int(version)
        type, bitstring = get_and_split(bitstring,3)
        type = to_int(type)
        bit_len = 6

        if type == 4:
            # literal value
            last_group = False
            number = ""
            while not last_group:
                group, bitstring = get_and_split(bitstring, 5)
                bit_len += 5
                if group[0] == "0":
                    last_group = True
                
                number += group[1:]
            
            number = to_int(number)
            # if bit_len % 4 != 0:
            #     padding = 4 - (bit_len %4)
            #     _, bitstring = get_and_split(bitstring, padding)
            #     bit_len += padding
            
            return LiteralPacket(version, type,bit_len, number), bitstring

        else:
            # operator
            len_type_id, bitstring = get_and_split(bitstring,1)
            bit_len += 1
            if len_type_id == "0":
                len, bitstring = get_and_split(bitstring, 15)
                bit_len += 15
                return OperatorPacket(version, type,bit_len, to_int(len_type_id), 0,to_int(len)), bitstring
            else:
                len, bitstring = get_and_split(bitstring, 11)
                bit_len += 11
                return OperatorPacket(version, type,bit_len, to_int(len_type_id),to_int(len),0), bitstring
            return 

    @classmethod
    def decode(cls,bitstring) -> Dict:

        parent_packet, bitstring = PacketDecoder.decode_packet(bitstring)

        if isinstance(parent_packet, LiteralPacket):
            return {parent_packet: None}, bitstring

        else:
            assert isinstance(parent_packet, OperatorPacket)
            if parent_packet.len_type == 0:
                packets = []
                sum_len = 0
                while sum_len < parent_packet.n_subbits:
                    packet, bitstring = PacketDecoder.decode(bitstring)
                    sum_len += count_bitlen(packet)
                    packets.append(packet)
                return {parent_packet: packets}, bitstring
            else: 
                
                packets = []
                for i in range(parent_packet.n_subpackats):
                    packet, bitstring = PacketDecoder.decode(bitstring)
                    packets.append(packet)
                return {parent_packet: packets}, bitstring
                



def count_versions(packet_dict):
    parent = list(packet_dict.keys())[0]

    if packet_dict[parent] == [] or packet_dict[parent] == None:
        return parent.version

    else:
        count = parent.version
        for packet in packet_dict[parent]:
            count += count_versions(packet)
        return count 

def count_bitlen(packet_dict):
    parent = list(packet_dict.keys())[0]

    if packet_dict[parent] == [] or packet_dict[parent] == None:
        return parent.bit_len

    else:
        count = parent.bit_len
        for packet in packet_dict[parent]:
            count += count_bitlen(packet)
        return count 
def part1(string):
    bitstring = str(bin(int(string,16)))[2:]
    if not len(bitstring) % 4 == 0:
        bitstring = "0" * (4- len(bitstring) % 4) + bitstring
    print(string)
    print(bitstring)
    packets, padding  =PacketDecoder.decode(bitstring)
    print( packets)
    
    print(count_versions(packets))
    
def operation(packet_dict):
    parent = list(packet_dict.keys())[0]
    if isinstance(parent, LiteralPacket):
        return parent.Literalvalue
    else:
        assert isinstance(parent, OperatorPacket)

        if parent.type == 0:
            return sum([operation(val) for val in packet_dict[parent]])
        if parent.type == 1:
            prod = 1
            for packet in packet_dict[parent]:
                prod *= operation(packet)
            return prod
        if parent.type ==2:
            return min([operation(val) for val in packet_dict[parent]])

        if parent.type == 3:
            return max([operation(val) for val in packet_dict[parent]])
        
        if parent.type == 5:
            return (operation(packet_dict[parent][0]) > operation(packet_dict[parent][1])) *1

        if parent.type == 6:
            return (operation(packet_dict[parent][0]) < operation(packet_dict[parent][1])) *1
        if parent.type == 7:
            return (operation(packet_dict[parent][0]) == operation(packet_dict[parent][1])) *1
        

def part2(string):
    bitstring = str(bin(int(string,16)))[2:]

    if not len(bitstring) % 4 == 0:
        bitstring = "0" * (4- len(bitstring) % 4) + bitstring
    print(string)
    print(bitstring)
    packets, padding  =PacketDecoder.decode(bitstring)
    print(packets)
    print(operation(packets))


if __name__ == "__main__":
    input_list = read_file(path = os.path.join(sys.path[0], "input.txt"))
    test_list = read_file(path = os.path.join(sys.path[0], "test_input.txt"))
    #part1(input_list[0])
    part2(input_list[0])