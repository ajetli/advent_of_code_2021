answer = 0
with open('input.txt') as f:
    lines = f.readlines()
    num_lines = len(lines)
    for i in range(0, num_lines - 3):
        cur = sum([int(l) for l in lines[i:i+3]])
        next = sum([int(l) for l in lines[i+1:i+4]])
        if next > cur:
            answer += 1
        print('line {} value {} current window {} vs. next window {}: answer {}'.format(
            i+1, int(lines[i]), cur, next, answer))

print(answer)
