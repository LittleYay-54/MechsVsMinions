from basislists import generate, permutation_generator
import itertools
from entities import Mech, Minion
from board import Board
from types import Vector


def engine(board: Board, position: Vector, bases: list):
    running_list = []
    for basis in bases:
        running_list += itertools.permutations(basis)
    for command_line in running_list:
        for direction in [[1,0], [-1,0], [0,-1], [0, 1]]:
            Mech(board, position, direction, command_line)
        

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cards = ['b', 'c', 'f', 'o', 'o', 'sk', 'sp']
    commandline_lengths = [6]
    bases = generate(cards, commandline_lengths)
