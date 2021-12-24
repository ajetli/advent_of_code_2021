from __future__ import annotations

import os
import pprint
from typing import Dict, List

file = 'input.txt'


class Cave:
    neighbors: List[Cave]
    val: str

    def __init__(self, val: str):
        self.val = val
        self.neighbors = []

    @property
    def is_large_cave(self):
        return self.val.isupper()

    @property
    def is_small_cave(self):
        return not self.is_large_cave

    @property
    def is_start(self):
        return self.val == 'start'

    @property
    def is_end(self):
        return self.val == 'end'

    def print(self):
        print('\nCurrent cave: {}'.format(self.val))
        print('Large cave: {}'.format(self.is_large_cave))
        print('Neighboring caves: {}'.format(
            [c.val for c in self.neighbors or []]))


class Cavern:
    caves: Dict[str, Cave]
    start: Cave

    def __init__(self, start, caves):
        self.caves = caves
        self.start = start

    def _dfs_print(self, current: Cave, visited: Dict[str, bool]):
        if current is not None:
            current.print()
            visited[current.val] = True
            for neighbor in current.neighbors:
                if not neighbor.val in visited:
                    self._dfs_print(neighbor, visited)

    def print(self):
        print('Printing cavern:')
        if not self.start:
            print('\nCavern is empty, no starting cave')
            return
        self._dfs_print(self.start, {})

    def _dfs_search_all_caves(
            self, curr_cave: Cave, path_so_far: List[str], all_paths: List[str], visited_small_twice: bool):
        # Go through all neighbors
        for neighbor in curr_cave.neighbors:
            # If this neighbor is the final destination, add to list of all paths
            if neighbor.is_end:
                path_so_far.append(neighbor.val)
                path = ','.join(path_so_far)
                all_paths.append(path)
            elif neighbor.is_large_cave:
                self._dfs_search_all_caves(
                    neighbor, path_so_far + [neighbor.val], all_paths, visited_small_twice)
            elif not neighbor.is_start:
                # If the next node is in your current path_so_far (repeating a small cave)
                # continue the recursion as long as you haven't visited other nodes twice already
                if neighbor.val in path_so_far and not visited_small_twice:
                    self._dfs_search_all_caves(
                        neighbor, path_so_far + [neighbor.val], all_paths, True)
                # If the neighbor is not in your path so far, continue
                elif neighbor.val not in path_so_far:
                    self._dfs_search_all_caves(
                        neighbor, path_so_far + [neighbor.val], all_paths, visited_small_twice)

    def search_all_caves(self):
        all_paths = []
        self._dfs_search_all_caves(
            self.start, [self.start.val], all_paths, False)
        return all_paths


# Parse input
lines = []
# Read input into map of Caves
start = None  # type: Cave
caves = {}    # type: Dict[str, Cave]
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]
    for line in lines:
        lhs = line.split('-')[0]
        rhs = line.split('-')[1]
        left_cave = caves.get(lhs)
        if not left_cave:
            left_cave = Cave(lhs)
        right_cave = caves.get(rhs)
        if not right_cave:
            right_cave = Cave(rhs)
        left_cave.neighbors.append(right_cave)
        right_cave.neighbors.append(left_cave)
        caves[lhs] = left_cave
        caves[rhs] = right_cave
        if left_cave.val == 'start':
            start = left_cave
        elif right_cave.val == 'start':
            start = right_cave

# Store input data as "cavern" which contains
# a mapping of each cave name to the cave data
# and the start cave
cavern = Cavern(start, caves)
cavern.print()

# Start a DFS going through all possible paths
all_paths = cavern.search_all_caves()
print('\nAll possible paths:')
pprint.pprint(all_paths)

print('\nSolution: {}'.format(len(all_paths)))
