from __future__ import annotations

import os
from functools import reduce
from typing import List

file = 'input_main.txt'


hex_to_bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

type_id_to_operator = {
    0: 'addition',
    1: 'multiplication',
    2: 'minimum',
    3: 'maximum',
    4: 'literal_value',
    5: 'greater_than',
    6: 'less_than',
    7: 'equal_to',
}


class Packet:
    version: int
    type_id: int
    depth: int = 0
    val: int = 0
    sub_packets: List[Packet] = []

    def __init__(self, version, type_id, depth):
        self.version = version
        self.type_id = type_id
        self.depth = depth

    def __repr__(self) -> str:
        formatted_sub_packets = ''
        for p in self.sub_packets:
            formatted_sub_packets += '\n{}{}'.format('\t'*self.depth, p)
        formatted_sub_packets = formatted_sub_packets or []
        return 'Packet({}, {}, {}, {})'.format(
            self.version,
            type_id_to_operator.get(self.type_id),
            self.val,
            formatted_sub_packets,
        )

    def get_value(self):
        # Addition
        if self.type_id == 0:
            v = 0
            for p in self.sub_packets:
                v += p.get_value()
            return v
        # Multiplication
        if self.type_id == 1:
            v = 1
            for p in self.sub_packets:
                v *= p.get_value()
            return v
        # Minimum
        if self.type_id == 2:
            v = float("inf")
            for p in self.sub_packets:
                v = min(v, p.get_value())
            return v
        # Maximum
        if self.type_id == 3:
            v = -1
            for p in self.sub_packets:
                v = max(v, p.get_value())
            return v
        # Literal
        elif self.type_id == 4:
            return self.val
        # Greater than
        if self.type_id == 5:
            return int(self.sub_packets[0].get_value() > self.sub_packets[1].get_value())
        # Less than
        if self.type_id == 6:
            return int(self.sub_packets[0].get_value() < self.sub_packets[1].get_value())
        # Equal
        if self.type_id == 7:
            return int(self.sub_packets[0].get_value() == self.sub_packets[1].get_value())


binary = ''
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines if l != '\n']
    # Iterate through each character in hexadecimal string and
    # append to binary string array
    for char in lines[0]:
        binary += hex_to_bin.get(char)

print('\nBinary string')
print(binary)

# Global variable to keep track of pointer
i = 0


def parse_packet(binary, depth):
    global i
    # Parse version
    version = int(binary[i:i+3], 2)
    i += 3
    # Parse type_id
    type_id = int(binary[i:i+3], 2)
    i += 3
    # Initialize packet
    packet = Packet(version, type_id, depth)
    # If type_id == 4, parse the literal and return
    if type_id == 4:
        found_last_group = False
        literal_val = ''
        while(not found_last_group):
            next_five = binary[i:i+5]
            literal_val += next_five[1:]
            if next_five[0] == '0':
                found_last_group = True
            i += 5
        packet.val = int(literal_val, 2)
    # Otherwise this is an operator, we may
    # have to parse sub-packets for this operator packet
    else:
        length_id_type = int(binary[i:i+1], 2)
        i += 1
        bits_to_parse = 15 if length_id_type == 0 else 11
        length = int(binary[i:i+bits_to_parse], 2)
        i += bits_to_parse
        sub_packets = []
        if length_id_type == 0:
            # If length id type is 0, parse "length" number of characters
            # which represents some arbitrary number of packets
            end = i + length
            while i < end:
                p = parse_packet(binary, depth+1)
                sub_packets.append(p)
        else:
            # If length id type is 1, parse "length" number of packets
            for _ in range(length):
                p = parse_packet(binary, depth+1)
                sub_packets.append(p)
        packet.sub_packets = sub_packets
    return packet


packet = parse_packet(binary, 1)
print(packet)
print('\nSolution: {}'.format(packet.get_value()))
