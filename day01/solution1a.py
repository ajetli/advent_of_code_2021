answer = 0
with open('input.txt') as f:
    lines = f.readlines()
    num_lines = len(lines)
    for i in range(0, num_lines - 1):
        j = i+1
        cur = int(lines[i])
        next = int(lines[j])
        if next > cur:
            answer += 1
        print('current depth {} vs. next depth {}: answer {}'.format(
            cur, next, answer))

print(answer)
