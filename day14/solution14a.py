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

# Start each step
curr_word = polymer_template
for i in range(10):
    next_word = ''
    for j in range(len(curr_word) - 1):
        pair = curr_word[j:j+2]
        # Add first letter to the new word
        next_word += pair[0]
        # If there is a pair insertion rule, add it next
        next_word += pair_insertion_rules.get(pair) or ''
        # If this is the "final pair" that is being processed, add the last character
        if j == len(curr_word) - 2:
            next_word += pair[1]
        # Continue
    curr_word = next_word
    print('After step {}: {}'.format(i + 1, curr_word))

counter_map = defaultdict(int)
for ch in curr_word:
    counter_map[ch] += 1

print('\nCharacter map')
pprint.pprint(counter_map)

solution = max(counter_map.values()) - min(counter_map.values())
print('\nSolution: {}'.format(solution))
