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

    def _dfs_search_all_caves(self, curr_cave: Cave, path_so_far: str, visited: Dict[str, bool], all_paths: List[str]):
        if curr_cave is not None:
            # Do not continue recursion if you have already visited this cave and are not supposed
            # to revisit this same cave
            if visited.get(curr_cave.val):
                return
            # If you have reached the end cave, add this path to your list of all paths
            if curr_cave.is_end:
                # Remove last trailing comma and add to result set
                path_so_far = path_so_far[:-1]
                all_paths.append(path_so_far)
                return
            # Otherwise recursively search all neighboring paths
            if not curr_cave.is_large_cave:
                visited[curr_cave.val] = True
            for neighbor in curr_cave.neighbors:
                self._dfs_search_all_caves(
                    neighbor, path_so_far + '{},'.format(neighbor.val), visited, all_paths)
            if not curr_cave.is_large_cave:
                del visited[curr_cave.val]

    def search_all_caves(self):
        all_paths = []
        self._dfs_search_all_caves(self.start, 'start,', {}, all_paths)
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
