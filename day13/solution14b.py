import os
import pprint
from collections import defaultdict
from typing import Dict

file = 'input_1.txt'


def print_grid(grid):
    for i in range(len(grid)):
        row = grid[i]
        l = ''
        for char in row:
            l += '#' if char else ' '
        print(l)


def replace_grid_row(grid, idx, new_row):
    grid[idx] = new_row
    return grid


def combine_lines(line1, line2):
    new_line = []
    for i in range(len(line1)):
        new_line.append(line1[i] or line2[i])
    return new_line


def get_grid_row(grid, i):
    return grid[i]


# Parse input
lines = []
dot_locations = []
max_row = -1
max_col = -1
fold_instructions = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines if l != '\n']
    # Parse all the dot locations on the paper
    i = 0
    while(len(lines[i].split(',')) == 2):
        x = int(lines[i].split(',')[1])
        y = int(lines[i].split(',')[0])
        # Get a list of all dot locations on the paper
        dot_locations.append((x, y))
        # Find number of rows in the paper
        max_row = x if x > max_row else max_row
        # Find number of columns in the paper
        max_col = y if y > max_col else max_col
        i += 1
    # Parse all the fold instructions
    for l in lines[i:]:
        axis = l.split('=')[0][-1]
        axis = 'row' if axis is 'y' else 'col'
        value = int(l.split('=')[1])
        fold_instructions.append((axis, value))

print('\nMax dimensions: ({},{})'.format(max_row + 1, max_col + 1))

# Build the grid
grid = [[False] * (max_col + 1) for _ in range(max_row + 1)]
for x, y in dot_locations:
    grid[x][y] = True

# Go through fold instructions
for instruction in fold_instructions:
    fold_type = instruction[0]
    index = instruction[1]
    # Fold along the row, change the size of the grid
    if fold_type == 'row':
        top = index - 1
        bottom = index + 1
        while(bottom < len(grid)):
            row1 = get_grid_row(grid, top)
            row2 = get_grid_row(grid, bottom)
            new_row = combine_lines(row1, row2)
            grid = replace_grid_row(grid, top, new_row)
            top -= 1
            bottom += 1
        # Truncate grid to new max number of rows
        grid = grid[:index]
    # Fold along the column, change the size of the grid
    else:
        left = index - 1
        right = index + 1
        while(right < len(grid[0])):
            # Replace each row's characters at "left" and "right" with
            # the correct expected value
            for i, row in enumerate(grid):
                row[right] = row[right] or row[left]
                grid[i] = row
            left -= 1
            right += 1
        # Truncate grid to the new max column for each row
        new_grid = []
        for row in grid:
            new_grid.append(row[index+1:])
        grid = new_grid

# Printing out the transparent paper final result
print('\nFinal grid:')
print_grid(grid)

# Reverse the image to read it properly
new_grid = []
for row in grid:
    i = 0
    j = len(row) - 1
    while i < j:
        row[i], row[j] = row[j], row[i]
        i += 1
        j -= 1
    new_grid.append(row)

print('\nFinal grid reversed:')
print_grid(new_grid)
