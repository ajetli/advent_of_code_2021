import os

power_consumption = 0
gamma_rate = ''
epsilon_rate = ''
# Each position in the array of length 12 has a pair
# array[i] indicates the count of 0s and 1s at position i in the bitstring
# pair[0] represents the count of 0s at this position, pair[1] represents counts of 1
bit_counts = []
for i in range(12):
    bit_counts.append([0, 0])

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        # Trim last \n character
        l = l[:-1]
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
        print('{}) Got binary string {}, bit_counts: {}'.format(
            i, l, bit_counts))

for pair in bit_counts:
    if pair[0] > pair[1]:
        gamma_rate += '0'
        epsilon_rate += '1'
    elif pair[1] > pair[0]:
        gamma_rate += '1'
        epsilon_rate += '0'
    else:
        print(
            'there was a tie in the number of 0s and 1s when computing gamma & epsilon rates')
        exit(1)

print('gamma rate {}, episilon rate {}'.format(gamma_rate, epsilon_rate))

print('gamma rate integer {}, episilon rate integer {}'.format(
    int(gamma_rate, 2), int(epsilon_rate, 2)))

power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
print('power consumption: {}'.format(power_consumption))
