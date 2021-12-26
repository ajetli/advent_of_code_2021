import os
from functools import reduce
from queue import PriorityQueue
from typing import List, Tuple

file = 'input_1.txt'


class Chiton:
    val: int
    low_risk_path: bool = False

    def __init__(self, val):
        self.val = val

    @property
    def val_with_color(self) -> str:
        if self.low_risk_path:
            return '\033[94m{}\033[0m'.format(str(self.val))
        else:
            return str(self.val)


class Cavern:
    grid: List[List[Chiton]]

    def __init__(self, grid):
        self.grid = grid

    @property
    def grid_size(self):
        return len(self.grid)

    def print(self):
        for row in self.grid:
            l = ''
            for chiton in row:
                l += ' {} '.format(chiton.val_with_color)
            print(l)

    def get_neighbor_coords(self, i: int, j: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
        # Return list of valid neighbors
        neighbors = []
        # Check up, down, left, and right as long as it's in bounds
        neighbor_positions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for neighbor in neighbor_positions:
            next_i = i + neighbor[0]
            next_j = j + neighbor[1]
            if next_i >= 0 and next_i < self.grid_size and next_j >= 0 and next_j < self.grid_size and not visited[next_i][next_j]:
                neighbors.append((next_i, next_j))
        return neighbors

    def explore_cavern(self):
        # Initialize the search at the top right corner
        start = (0, 0)
        cost = 0
        full_path = [start]
        # Keep track of which nodes you have already visited
        visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        pq = PriorityQueue()
        pq.put((cost, start, full_path))
        visited[0][0] = True
        while not pq.empty():
            cost, node, full_path = pq.get()
            x, y = node
            neighbor_coords = self.get_neighbor_coords(x, y, visited)
            for next_x, next_y in neighbor_coords:
                neighbor = self.grid[next_x][next_y]
                # If we have reached the end, return
                if next_x == self.grid_size - 1 and next_y == self.grid_size - 1:
                    print('\nFound lowest risk path to end of the cave!')
                    full_path += [(next_x, next_y)]
                    for x, y in full_path:
                        self.grid[x][y].low_risk_path = True
                    self.print()
                    print('\nSolution: {}'.format(cost + neighbor.val))
                    return
                # Otherwise continue the search
                pq.put((cost + neighbor.val, (next_x, next_y),
                       full_path + [(next_x, next_y)]))
                visited[next_x][next_y] = True


# Parse input
grid = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]
    for i, line in enumerate(lines):
        grid.append([])
        for char in line:
            grid[i].append(Chiton(int(char)))

cavern = Cavern(grid)
cavern.explore_cavern()
