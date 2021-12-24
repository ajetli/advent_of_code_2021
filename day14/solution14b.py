import os
import pprint
from collections import defaultdict
from typing import Dict

file = 'input_1.txt'

# Parse input
polymer_template = ''     # type: str
pair_insertion_rules = {}  # type: Dict[str, str]
lines = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines if l != '\n']
    for i, l in enumerate(lines):
        if i == 0:
            polymer_template = l
            continue
        pair = l.split(' -> ')
        pair_insertion_rules[pair[0]] = pair[1]

print('\nPolymer Template:')
print(polymer_template)

print('\nPair insertion rules:')
pprint.pprint(pair_insertion_rules)

# Convert polymer template into counts for each pair of characters
cur_pair_count = defaultdict(int)
for i in range(len(polymer_template) - 1):
    pair = polymer_template[i:i+2]
    cur_pair_count[pair] += 1

# Start each step
for i in range(40):
    next_pair_count = defaultdict(int)
    for pair, count in cur_pair_count.items():
        insert = pair_insertion_rules.get(pair)
        # If there are no pair insertion rules for k, continue
        if not insert:
            next_pair_count[pair] += count
        # Add new counts for current pair
        else:
            left = pair[0] + insert
            right = insert + pair[1]
            next_pair_count[left] += count
            next_pair_count[right] += count
    cur_pair_count = next_pair_count
    print('\nPair counts after step {}:'.format(i+1))
    pprint.pprint(cur_pair_count)

# Get counts of each character
char_counts = defaultdict(int)
for pair, count in cur_pair_count.items():
    char_counts[pair[0]] += count
    char_counts[pair[1]] += count

# Account for duplicates in this process by adding 1 then dividing by 2
char_counts_adj = defaultdict(int)
for char, count in char_counts.items():
    char_counts_adj[char] = int((count + 1) / 2)

print('\nCharacter counts:')
pprint.pprint(char_counts_adj)

solution = max(char_counts_adj.values()) - min(char_counts_adj.values())
print('\nSolution: {}'.format(solution))
