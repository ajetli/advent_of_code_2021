import os

solution = [0, 0]
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()
    directionMap = {
        'forward': (0, 1),
        'down': (1, 1),
        'up': (1, -1),
    }
    for index, l in enumerate(lines):
        split = l.split()
        direction = split[0]
        value = int(split[1])
        i, j = directionMap.get(direction)
        solution[i] += value * j
        print('{}) {}: horizontal position {} vertical position {}'.format(
            index+1, l[:-1], solution[0], solution[1]))


print('Final Solution) horizontal position {} vertical position {} solution {}'.format(
    solution[0], solution[1], solution[0] * solution[1]))
