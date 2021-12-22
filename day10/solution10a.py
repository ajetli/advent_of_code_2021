import os

file = 'input.txt'

# Parse input
lines = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]

# Iterate through each line & count if it is invalid
closed_to_open_bracket = {
    ')': ['(', 3],
    ']': ['[', 57],
    '}': ['{', 1197],
    '>': ['<', 25137],
}


solution = 0
for line in lines:
    stack = []
    for i, char in enumerate(line):
        if char in ['(', '[', '{', '<']:
            stack.append(char)
        else:
            previous_open = stack.pop()
            expected_open = closed_to_open_bracket.get(char)
            if expected_open and expected_open[0] != previous_open:
                solution += expected_open[1]
                print('Found incorrect line, first matching incorrect character at position {}: {}'.format(
                    i, char))
                print(line)
    if len(stack) > 0:
        print('Incomplete line: {}'.format(line))

print('\nSolution: {}'.format(solution))
