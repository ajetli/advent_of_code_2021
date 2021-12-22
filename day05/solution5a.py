import os
import pprint
from typing import List, Tuple

grid_size = 1000


def print_grid(grid: List[List[int]]):
    for i in range(len(grid)):
        l = ''
        for j in range(len(grid[i])):
            l += ' {} '.format(str(grid[i][j]))
        l = l[:-1]
        print(l)


# Parse files
lines = []
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines if l != '\n']

# Create a empty grid based on range of numbers in pairs
grid = []  # type: List[List[int]]
for i in range(grid_size):
    grid.append([])
    for j in range(grid_size):
        grid[i].append(0)

# Convert text lines into list of coordinate pairs
coordinates = []  # type: List[Tuple[Tuple]]
for l in lines:
    # Note: problem inverts x & y coordinates so this is why we're fixing it
    lhs = l.split(' ->')[0]
    left_coords = (int(lhs.split(',')[1]), int(lhs.split(',')[0]))
    rhs = l.split('-> ')[1]
    right_coords = (int(rhs.split(',')[1]), int(rhs.split(',')[0]))
    coordinates.append((left_coords, right_coords))

print('coordinates:')
pprint.pprint(coordinates)

# Iterate through coordinate pairs and find pipelines
# which are vertical + horizontal and mark them in the grid
for i in range(len(coordinates)):
    left_coord, right_coord = coordinates[i]
    x1, y1 = left_coord
    x2, y2 = right_coord
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            grid[x1][i] += 1
    if y1 == y2:
        for i in range(min(x1, x2), max(x1, x2) + 1):
            grid[i][y1] += 1

solution = 0
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] > 1:
            solution += 1

# print_grid(grid)

print('Solution: {}'.format(solution))
