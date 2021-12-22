import os
import sys

file = 'input.txt'

# Parse files
crab_positions = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    crab_positions = [int(x) for x in lines[0].split(',')]

# Get the min and max crab position for the binary search
l = min(crab_positions)
r = max(crab_positions)


def compute_fuel_consumption(crab_positions, position):
    # Iterate through each crab's position & add to the total fuel consumption
    # based on the formula (N * N+1) / 2
    fuel_consumption = 0
    for crab in crab_positions:
        fuel_consumption += int((abs(crab - position) *
                                 (abs(crab - position) + 1) / 2))
    print('Fuel efficiency of position {} is: {}'.format(
        position, fuel_consumption))
    return fuel_consumption


# Find the lowest fuel consumption position
min_fuel_consumption = float("inf")
optimal_position = -1
while l < r:
    fuel_consumption_l = compute_fuel_consumption(crab_positions, l)
    fuel_consumption_r = compute_fuel_consumption(crab_positions, r)
    if fuel_consumption_l < fuel_consumption_r:
        # Mark down the optimal position so far & optimal fuel consumption so far
        optimal_position = l
        min_fuel_consumption = min(min_fuel_consumption, fuel_consumption_l)
        # Continue binary search
        r = int((l + r) / 2)
    else:
        # Mark down the optimal position so far & optimal fuel consumption so far
        optimal_position = r
        min_fuel_consumption = min(min_fuel_consumption, fuel_consumption_r)
        # Continue binary search
        l = int((l + r) / 2)

print('Optimal position: {}'.format(optimal_position))
print('Minimum fuel consumption: {}'.format(min_fuel_consumption))
