import os
import pprint
from collections import defaultdict
from typing import Dict, List


class BoardPosition:
    val: int
    marked: bool = False

    def __init__(self, val: int):
        self.val = val


class Board:
    board: List[List[BoardPosition]]
    board_dimension: int = 5

    def __init__(self, board):
        self.board = board

    def print(self):
        """
        Prints out which positions are marked on the board (highlighted in color)
        """
        for i in range(self.board_dimension):
            l = ''
            for j in range(self.board_dimension):
                val = self.board[i][j].val
                marked = self.board[i][j].marked
                if val < 10:
                    l += ' '
                if marked:
                    l += ' \033[94m{}\033[0m '.format(str(val))
                else:
                    l += ' {} '.format(str(val))
            l = l[:-1]
            print(l)

    def is_solved(self):
        """
        Checks whether the current state of the board is solved
        """
        # Go through all 5 rows
        for i in range(self.board_dimension):
            row = self.board[i]
            if all([x.marked for x in row]):
                return True
        # Go through all 5 columns
        for j in range(self.board_dimension):
            col = [self.board[i][j] for i in range(self.board_dimension)]
            if all([x.marked for x in col]):
                return True
        # Go through 2 diagonals
        diagonal_1 = [self.board[i][i] for i in range(self.board_dimension)]
        if all([x.marked for x in diagonal_1]):
            return True
        diagonal_2 = [self.board[self.board_dimension - 1 - i][i]
                      for i in range(self.board_dimension)]
        if all([x.marked for x in diagonal_2]):
            return True
        # Board is not finished yet
        return False

    def sum_of_unmarked(self):
        res = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if not self.board[i][j].marked:
                    res += self.board[i][j].val
        return res


def print_all_boards(boards: Dict[int, Board]):
    for i, board in boards.items():
        print('\nBoard {}'.format(i))
        board.print()


# Parse file into array of lines, removing unneccessary new lines
lines = []
with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()
    lines = [l[:-1] for l in lines if l != '\n']

# The list of numbers that the BINGO announcer will call in order
numbers_to_call = [int(x)
                   for x in lines[0].split(',')]  # type: List[int]
print('numbers_to_call:')
pprint.pprint(numbers_to_call)

# List of BINGO boards by index
# {
#     0: [
#           [1, 2, 3, 4, 5],
#           [1, 2, 3, 4, 5],
#           [1, 2, 3, 4, 5],
#           [1, 2, 3, 4, 5],
#           [1, 2, 3, 4, 5],
#        ],
#     1: [...]
# }
boards = {}  # type: Dict[int, Board]

# Mapping of number to the boards that contain the number + positions
# {
#     1: [(0, 1, 3), (1, 3, 2)]
# }
number_to_position = defaultdict(list)  # type: Dict[int, List]

# Create the boards & number_to_position mappings
board_index = 0
for i in range(1, len(lines), 5):
    # Parse from string format to "Board" object
    board = []
    for j in range(5):
        board.append([])
        for x in lines[i+j].split(' '):
            if x.isdigit():
                board[j].append(BoardPosition(int(x)))
    # Add board to the board map
    boards[board_index] = Board(board)
    # Iterate through the board to get the number_to_position map
    for x in range(len(board)):
        for y in range(len(board[x])):
            number_to_position[board[x][y].val].append((board_index, x, y))
    # Continue parsing board
    board_index += 1

# Start going through the numbers
for number in numbers_to_call:
    # Find all boards & positions which use that number
    positions_with_number = number_to_position.get(number) or []
    for position in positions_with_number:
        board_index = position[0]
        row = position[1]
        col = position[2]
        # Mark position on the board
        board = boards.get(board_index)
        if board is not None:
            board.board[row][col].marked = True
            if board.is_solved():
                print('\nSolved one of the boards!')
                print('Number called: {}'.format(number))
                print('Board: {}'.format(board_index))
                board.print()
                sum_unmarked = board.sum_of_unmarked()
                print('Sum of remaining numbers: {}'.format(sum_unmarked))
                print('Final Solution: {}'.format(sum_unmarked * number))
                exit(1)
    print('\nCalling number {}, printing out all boards:'.format(number))
    print_all_boards(boards)
