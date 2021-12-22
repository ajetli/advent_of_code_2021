import os

life_support_rating = 0
oxygen_generator_rating = ''
c02_scrubber_rating = ''


def initialize_bit_counts():
    # Each position in the array of length 12 has a pair
    # array[i] indicates the count of 0s and 1s at position i in the bitstring
    # pair[0] represents the count of 0s at this position, pair[1] represents counts of 1
    bit_counts = []
    for i in range(12):
        bit_counts.append([0, 0])
    return bit_counts


# This function parses a list of bit array strings and returns
# the bit counts at each position
def compute_bit_counts(lines):
    bit_counts = initialize_bit_counts()
    for l in lines:
        # Go through each character in string
        for j, c in enumerate(l):
            if c is '0':
                bit_counts[j][0] += 1
            elif c is '1':
                bit_counts[j][1] += 1
            else:
                print(
                    'got invalid input, unexpected character {} in string: {}'.format(c, l))
                exit(1)
    return bit_counts


# Parse input file
lines = []
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]
    for i, l in enumerate(lines):
        # Trim last \n character
        l = l[:-1]

o_list = lines
for i in range(12):
    print('o_list, current size: {}'.format(len(o_list)))
    # If the list is not size 0, find the max bit at position i
    bit_counts = compute_bit_counts(o_list)
    # If there are more 1s than 0s at position i in the current list
    # filter the list to only include the lines which have 1 at position i
    print('position {}) count 0s {}, count 1s {}'.format(
        i, bit_counts[i][0], bit_counts[i][1]))
    if bit_counts[i][1] >= bit_counts[i][0]:
        o_list = [l for l in o_list if l[i] == '1']
    else:
        o_list = [l for l in o_list if l[i] == '0']
    print('filtered o_list, current size: {}'.format(len(o_list)))
    # If o_list is size 1, return
    if len(o_list) == 1:
        oxygen_generator_rating = o_list[0]
        break

c_list = lines
for i in range(12):
    print('c_list, current size: {}'.format(len(c_list)))
    # If the list is not size 0, find the max bit at position i
    bit_counts = compute_bit_counts(c_list)
    # If there are more 1s than 0s at position i in the current list
    # filter the list to only include the lines which have 1 at position i
    print('position {}) count 0s {}, count 1s {}'.format(
        i, bit_counts[i][0], bit_counts[i][1]))
    if bit_counts[i][0] <= bit_counts[i][1]:
        c_list = [l for l in c_list if l[i] == '0']
    else:
        c_list = [l for l in c_list if l[i] == '1']
    print('filtered c_list, current size: {}'.format(len(c_list)))
    # Reduce c_list to size 1
    if len(c_list) == 1:
        c02_scrubber_rating = c_list[0]
        break

print('oxygen_generator_rating: {}, c02_scrubber_rating: {}'.format(
      oxygen_generator_rating, c02_scrubber_rating))

print('life_support_rating: {}'.format(
    int(oxygen_generator_rating, 2) * int(c02_scrubber_rating, 2)
))
