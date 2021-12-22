import os

file = 'input.txt'

# Parse input
lines = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]

# count number of times 1, 4, 7, or 8 happen
count = 0
for line in lines:
    rhs = [sorted(w) for w in line.split('|')[1].strip().split(' ')]
    lhs = [sorted(w) for w in line.split('|')[0].strip().split(' ')]
    for word in rhs:
        if len(word) in [2, 3, 4, 7]:
            count += 1

print('Solution: {}'.format(count))
