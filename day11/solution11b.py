import os
from functools import reduce
from typing import List, Tuple

file = 'input.txt'
grid_size = 10


class Octopus:
    val: int

    def __init__(self, val):
        self.val = val

    def val_with_color(self) -> str:
        return str(self.val) if self.val else '\033[94m{}\033[0m'.format(self.val)


class Cavern:
    grid: List[List[Octopus]]

    def __init__(self, grid):
        self.grid = grid

    def print(self):
        for row in self.grid:
            l = ''
            for octopus in row:
                l += ' {} '.format(octopus.val_with_color())
            print(l)

    def is_fully_lit(self):
        for x in range(grid_size):
            for y in range(grid_size):
                if self.grid[x][y].val != 0:
                    return False
        return True


def get_neighbors(octopus_coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    # Return list of valid neighbors
    neighbors = []
    # Check all adjacent squares as long as they are in bounds
    neighbor_positions = [
        (0, -1),    # W
        (0, 1),     # E
        (1, 0),     # S
        (-1, 0),    # N
        (-1, -1),   # NW
        (1, -1),    # NE
        (-1, 1),    # SW
        (1, 1),     # SE
    ]
    for x, y in neighbor_positions:
        next_x = octopus_coords[0] + x
        next_y = octopus_coords[1] + y
        if next_x >= 0 and next_x < grid_size and next_y >= 0 and next_y < grid_size:
            neighbors.append((next_x, next_y))
    return neighbors


# Parse input
grid = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]
    for i, line in enumerate(lines):
        grid.append([])
        for char in line:
            grid[i].append(Octopus(int(char)))

print('\nCavern before any steps:')
cavern = Cavern(grid)
cavern.print()

solution = 0
for i in range(10000):
    # This is a list of tuples (octopus positions on grid)
    # that will flash this round
    octopuses_to_flash = []
    # Keep track of octopuses that we have visited this round
    # to avoid re-adding them to the list
    visited_octopuses = [[False] * grid_size for _ in range(grid_size)]
    # First increment all octopus' counts by 1
    for x in range(grid_size):
        for y in range(grid_size):
            cavern.grid[x][y].val += 1
            if cavern.grid[x][y].val > 9:
                visited_octopuses[x][y] = True
                octopuses_to_flash.append((x, y))
    # Then go through each octopus that should flash and find all
    # of it's neighbors. Increment the counts of each of it's neighbors
    # by 1 and add a neighbor to the list of octopuses to flash if its count
    # is greater than 10
    while len(octopuses_to_flash) > 0:
        octopus_coords = octopuses_to_flash.pop()
        for x, y in get_neighbors(octopus_coords):
            cavern.grid[x][y].val += 1
            if not visited_octopuses[x][y] and cavern.grid[x][y].val > 9:
                visited_octopuses[x][y] = True
                octopuses_to_flash.append((x, y))
    # Finally, decrement the count of each octopus that flashed to 0
    for x in range(grid_size):
        for y in range(grid_size):
            if cavern.grid[x][y].val > 9:
                cavern.grid[x][y].val = 0
    print('\nCavern after step {}:'.format(i + 1))
    cavern.print()
    # Check if all octopuses are flashing at the same time, if so
    # this is the step for your final solution
    if cavern.is_fully_lit():
        solution = i + 1
        break

print('\nSolution: {}'.format(solution))
