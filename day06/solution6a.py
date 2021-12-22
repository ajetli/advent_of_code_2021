import os

file = 'input.txt'

# Parse files
lines = []
lanternfish_counters = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lanternfish_counters = [int(x) for x in lines[0].split(',')]

print('Initial state) number of lanternfish: {}'.format(
    len(lanternfish_counters)))

for i in range(80):
    # Each day find the number of fish we need to add
    count_fish_to_add = 0
    # For each fish, if the counter reaches 0 reset it to 6 and "add"
    # a new fish to the total list
    for j in range(len(lanternfish_counters)):
        if lanternfish_counters[j] == 0:
            count_fish_to_add += 1
            lanternfish_counters[j] = 6
        else:
            lanternfish_counters[j] -= 1
    # Add new lanternfish to the list
    lanternfish_counters += [8] * count_fish_to_add
    # Print the tally at the end of the day
    print('After day {}) number of lanternfish: {}'.format(
        i + 1, len(lanternfish_counters)))
