import os

file = 'input.txt'

# Parse input
lines = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]

# Mapping of each closed bracket to it's corresponding open bracket
closed_to_open_bracket = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

# Reverse mapping of open to close
open_to_closed_bracket = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


# Mapping of each open bracket to the "points"
open_bracket_points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

solutions = []
for line in lines:
    stack = []
    invalid_line = False
    for i, char in enumerate(line):
        if char in ['(', '[', '{', '<']:
            stack.append(char)
        else:
            previous_open = stack.pop()
            expected_open = closed_to_open_bracket.get(char)
            if expected_open and expected_open[0] != previous_open:
                invalid_line = True
                break
    # The line is incomplete if there are remaining characters on
    # the stack and the line was not invalid
    if not invalid_line and len(stack) > 0:
        print('\nFound incomplete line with {} remaining characters'.format(len(stack)))
        points_for_line = 0
        completed_line = ''
        while len(stack) > 0:
            next_open = stack.pop()
            completed_line += open_to_closed_bracket.get(next_open)
            points_for_line *= 5
            points_for_line += open_bracket_points.get(next_open) or 0
        print('Incomplete line can be completed with: {}'.format(completed_line))
        print('This line completion is worth {} points'.format(str(points_for_line)))
        solutions.append(points_for_line)

solutions = sorted(solutions)
print('Points for each autocompletion: {}'.format(solutions))

midpoint = int((len(solutions) - 1) / 2)
print('\nSolution: {}'.format(solutions[midpoint]))
