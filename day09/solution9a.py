import os
import pprint
from typing import List

file = 'input.txt'
grid_size = 100


class GridPosition:
    val: int
    low_point: bool = False

    def __init__(self, val):
        self.val = val


class Grid:
    grid: List[List[GridPosition]]

    def __init__(self, grid):
        self.grid = grid

    def print(self):
        for row in self.grid:
            l = ''
            for gp in row:
                if gp.low_point:
                    l += ' \033[94m{}\033[0m '.format(str(gp.val))
                else:
                    l += ' {} '.format(str(gp.val))
            print(l)


# Parse input
grid = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]
    for i, line in enumerate(lines):
        grid.append([])
        for char in line:
            grid[i].append(GridPosition(int(char)))

grid = Grid(grid)

# Iterate through the grid and find out if each grid position is a low_point
solution = 0
for i in range(grid_size):
    for j in range(grid_size):
        # Current grid position
        gp = grid.grid[i][j]
        # Check up, down, left, and right as long as it's in bounds
        neighbors = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        low_point = True
        for x, y in neighbors:
            next_i = i + x
            next_j = j + y
            if next_i >= 0 and next_i < grid_size and next_j >= 0 and next_j < grid_size:
                next_gp = grid.grid[next_i][next_j]
                if next_gp.val <= gp.val:
                    low_point = False
                    break
        # Mark grid position as a low point, add to the solution, continue
        grid.grid[i][j].low_point = low_point
        solution += gp.val + 1 if low_point else 0

print('\nFinal grid')
grid.print()
print('\nSolution: {}'.format(solution))
