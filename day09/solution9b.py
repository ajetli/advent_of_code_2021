import os
from functools import reduce
from typing import List, Tuple

file = 'input.txt'
grid_size = 100


class GridPosition:
    val: int
    low_point: bool = False
    in_basin: bool = False

    def __init__(self, val):
        self.val = val

    def get_value_with_color(self) -> str:
        if self.low_point:
            return '\033[94m{}\033[0m'.format(str(self.val))
        elif self.in_basin:
            return '\033[91m{}\033[0m'.format(str(self.val))
        else:
            return str(self.val)


class Grid:
    grid: List[List[GridPosition]]

    def __init__(self, grid):
        self.grid = grid

    def print(self):
        for row in self.grid:
            l = ''
            for gp in row:
                l += ' {} '.format(gp.get_value_with_color())
            print(l)


def get_neighbors(i: int, j: int) -> List[Tuple[int, int]]:
    # Return list of valid neighbors
    neighbors = []
    # Check up, down, left, and right as long as it's in bounds
    neighbor_positions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    for neighbor in neighbor_positions:
        next_i = i + neighbor[0]
        next_j = j + neighbor[1]
        if next_i >= 0 and next_i < grid_size and next_j >= 0 and next_j < grid_size:
            neighbors.append((next_i, next_j))
    return neighbors


def explore_basin(grid: Grid, i: int, j: int) -> int:
    # Do not visit nodes you have already visited before, starting from the low point
    visited = [[False] * grid_size for _ in range(grid_size)]
    visited[i][j] = True
    neighbors = get_neighbors(i, j)
    # Continue DFS iterating through all neighbors starting at low point
    basin_size = 1
    while len(neighbors) > 0:
        next_i, next_j = neighbors.pop()
        # Do not re-process nodes we have already visited
        if visited[next_i][next_j]:
            continue
        visited[next_i][next_j] = True
        # Do not continue iterating if the basin contains a 9
        if grid.grid[next_i][next_j].val == 9:
            continue
        # Otherwise, mark this as a node in the basin, add all it's
        # neighbors to the DFS and continue
        grid.grid[next_i][next_j].in_basin = True
        basin_size += 1
        neighbors += get_neighbors(next_i, next_j)
    return basin_size


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
basin_sizes = []
for i in range(grid_size):
    for j in range(grid_size):
        # Current grid position
        gp = grid.grid[i][j]
        low_point = True
        neighbors = get_neighbors(i, j)
        for next_i, next_j in neighbors:
            next_gp = grid.grid[next_i][next_j]
            if next_gp.val <= gp.val:
                low_point = False
                break
        # Mark grid position as a low point, do another DFS to mark all neighbor
        # positions as basins
        if low_point:
            grid.grid[i][j].low_point = low_point
            basin_sizes.append(explore_basin(grid, i, j))

print('\nFinal grid')
grid.print()

basin_sizes = sorted(basin_sizes)
print('\nBasin sizes: {}'.format(basin_sizes))

top_three = basin_sizes[-3:]
solution = reduce(lambda x, y: x * y, top_three)
print('\nSolution: {}'.format(solution))
