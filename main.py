import numpy as np
from custom_types import Vector, Matrix
from basislists import generate
from typing import List
from entities import Mech
from board import Board
from game_flow import initialize_starting_board
from copy import deepcopy
from engine import engine
from itertools import permutations


if __name__ == '__main__':
    # Anson do your thing here
    # I have functions that will initialize a board state in game_flow.py
    # for every basis list, create a board with the minions and the oil
    # and instantiate a Mech (which automatically places it on the board)

    # you can try to run the engine for each of these, but there are probably a morbillion bugs
    # i'll look at them later unless you can figure out how to fix the code

    mech_list: List[Mech] = []

    # for basis_list in generate(['Blaze', 'Cyclotron', 'Flamespitter', 'Omnistomp', 'Omnistomp', 'Skewer', 'Speed'], [5]):
    #   make mechs with specific cmd lines here

    base_board: Board = Board(np.zeros((6, 6)))
    starting_minions: Matrix = np.array(
        [
            [0, 2],
            [1, 2],
            [2, 0],
            [2, 1],
            [2, 4],
            [5, 2]
        ]
    )
    starting_oil: Matrix = np.array(
        [
            [2, 2],
            [2, 3],
            [3, 2],
            [3, 3]
        ]
    )
    initialize_starting_board(base_board, starting_minions, starting_oil)

    command_lines = []
    for basis_list in generate(['Blaze', 'Cyclotron', 'Flamespitter', 'Omnistomp', 'Omnistomp', 'Skewer', 'Speed'], [6]):
        command_lines += permutations(basis_list)

    Tristanas = []
    for cmd_line in command_lines:
        Right_Tristana = Mech(deepcopy(base_board), np.array([4, 4]), np.array([1, 0]), 'Right')
        for i in range(len(cmd_line)):
            if cmd_line[i] in {'Blaze', 'Cyclotron', 'Flamespitter', 'Omnistomp', 'Skewer', 'Speed'}:
                Right_Tristana.modify_command_line(i, cmd_line[i])
            else:
                level = int(cmd_line[i][-1])
                command = cmd_line[i][:-1]
                Right_Tristana.modify_command_line(i, command, level)
        Up_Tristana = deepcopy(Right_Tristana)
        Up_Tristana.turn(90)
        Up_Tristana.name = 'Up'
        Left_Tristana = deepcopy(Up_Tristana)
        Left_Tristana.turn(90)
        Left_Tristana.name = 'Left'
        Down_Tristana = deepcopy(Left_Tristana)
        Down_Tristana.turn(90)
        Down_Tristana.name = 'Down'
        Tristanas += [Right_Tristana, Up_Tristana, Left_Tristana, Down_Tristana]

    trist_num = 0
    for Tristana in Tristanas:
        engine(Tristana.board, Tristana)
        trist_num += 1
        print(f"A Tristana has been resolved. #{trist_num}")

