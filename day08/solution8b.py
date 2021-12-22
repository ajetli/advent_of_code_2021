import os
import pprint

file = 'input.txt'

# Parse input
lines = []
with open(os.path.join(os.path.dirname(__file__), file)) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines]

# count number of times 1, 4, 7, or 8 happen
solution = 0
for line in lines:
    print('\nParsing line: {}'.format(line))
    rhs = [''.join(sorted(w)) for w in line.split('|')[1].strip().split(' ')]
    lhs = [''.join(sorted(w)) for w in line.split('|')[0].strip().split(' ')]
    word_to_number = {}
    number_to_word = {}
    # Iterate through all words to find 1, 4, 7, and 8
    for word in rhs + lhs:
        if len(word) == 2:
            word_to_number[word] = 1
            number_to_word[1] = word
        elif len(word) == 3:
            word_to_number[word] = 7
            number_to_word[7] = word
        elif len(word) == 4:
            word_to_number[word] = 4
            number_to_word[4] = word
        elif len(word) == 7:
            word_to_number[word] = 8
            number_to_word[8] = word
        else:
            word_to_number[word] = -1
    # Take a 2nd pass to find more numbers
    for word in rhs + lhs:
        four = number_to_word[4]
        seven = number_to_word[7]
        if len(word) == 6:
            # Number 9 will contain all characters in 4 and is of length 6
            if set(four).issubset(word):
                word_to_number[word] = 9
                number_to_word[9] = word
            # If we subtract all characters from 7 from all characters
            # in numbers 0 and 6, it will have different lengths of
            # remaining characters
            elif len(set(word) - set(seven)) == 3:
                word_to_number[word] = 0
                number_to_word[0] = word
            elif len(set(word) - set(seven)) == 4:
                word_to_number[word] = 6
                number_to_word[6] = word
        if len(word) == 5:
            # Number 2 will have 3 characters different between itself and 4
            if len(set(word) - set(four)) == 3:
                word_to_number[word] = 2
                number_to_word[2] = word
            # Number 3 will only have 2 characters different between itself and 7
            elif len(set(word) - set(seven)) == 2:
                word_to_number[word] = 3
                number_to_word[3] = word
            # Number 5 will have 3 characters different between itself 7
            elif len(set(word) - set(seven)) == 3:
                word_to_number[word] = 5
                number_to_word[5] = word
    print('Word to number mappings')
    pprint.pprint(word_to_number)
    input = ''
    for word in lhs:
        number = word_to_number[word]
        input += str(number)
    output = ''
    for word in rhs:
        number = word_to_number[word]
        output += str(number)
    print('Converted line: {} | {}'.format(input, output))
    solution += int(output)
    print('Solution so far: {}'.format(solution))

print('\nFinal solution: {}'.format(solution))
