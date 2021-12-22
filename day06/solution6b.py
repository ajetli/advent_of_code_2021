import os
from collections import defaultdict

file = 'input.txt'

# Parse files
lines = []
lanternfish_counter_map = defaultdict(int)
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lanternfish = [int(x) for x in lines[0].split(',')]
    for fish in lanternfish:
        lanternfish_counter_map[fish] += 1

print('Initial state) number of laternfish: {}'.format(
    sum([v for v in lanternfish_counter_map.values()])))

for day in range(256):
    # Create new map which contains count of each fish
    # If old map had 23 fish with count 1, new map will have 23 fish with count 0
    new_lanternfish_counter_map = defaultdict(int)
    # Construct new counts
    for i, num_fish in lanternfish_counter_map.items():
        if i == 0:
            new_lanternfish_counter_map[6] += num_fish
            new_lanternfish_counter_map[8] += num_fish
        else:
            new_lanternfish_counter_map[i - 1] += num_fish
    # Re-assign new count map to old count map
    lanternfish_counter_map = new_lanternfish_counter_map
    print('After day {}) number of laternfish: {}'.format(
        day+1, sum([v for v in lanternfish_counter_map.values()])))
