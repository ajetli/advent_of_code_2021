from __future__ import annotations

import os
from functools import reduce
from typing import List

file = 'input_0.txt'


class Packet:
    type_id: int
    version: int
    packets: List[Packet]
    val: int

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

    def get_value(self):
        if self.type_id == 4:
            return self.val


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


def parse_binary(binary):
    i = 0
    packets = []
    while i < len(binary) and int(binary[i:], 2) > 0:
        # Parse version
        version = int(binary[i:i+3], 2)
        i += 3
        # Parse type_id
        type_id = int(binary[i:i+3], 2)
        i += 3
        packet = Packet(version, type_id)
        # If type_id == 4, parse the literal
        if type_id == 4:
            found_last_group = False
            literal_val = ''
            while(not found_last_group):
                next_five = binary[i:i+5]
                if next_five[0] == '0':
                    found_last_group = True
                    literal_val += next_five[1:]
                i += 5
            packet.val = int(literal_val, 2)
            packets.append(packet)
        else:
            # Otherwise this is an operator
            length_id_type = int(binary[i:i+1])
            i += 1
            bits_to_parse = 15 if length_id_type == 0 else 11
            length = int(binary[i:i+bits_to_parse])
            i += bits_to_parse
            packet.packets = parse_binary(binary[i:i+length])
            packets.append(packet)
            i += length
    return packets


packets = parse_binary(binary)
print(len(packets))
