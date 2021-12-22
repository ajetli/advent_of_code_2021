import os

solution = [0, 0]
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()
    aim = 0
    for index, l in enumerate(lines):
        split = l.split()
        direction = split[0]
        value = int(split[1])
        if direction == 'forward':
            solution[0] += value
            solution[1] += aim * value
        elif direction == 'down':
            aim += value
        elif direction == 'up':
            aim -= value
        else:
            continue
        print('{}) {}: horizontal position {} vertical position {} aim {}'.format(
            index+1, l[:-1], solution[0], solution[1], aim))

print('Final Solution) horizontal position {} vertical position {} solution {}'.format(
    solution[0], solution[1], solution[0] * solution[1]))
