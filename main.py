import numpy as np
from custom_types import Vector, Matrix
from basislists import generate
from typing import List
from entities import Mech
from board import Board
from game_flow import initialize_starting_board
from copy import deepcopy
from engine import engine

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

    board: Board = Board(np.zeros((6, 6)))
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
    initialize_starting_board(board, starting_minions, starting_oil)

    Tristana_1 = Mech(board, np.array([4, 4]), np.array([1, 0]), 'Right')
    Tristana_1.modify_command_line(1, 'Blaze', 2)
    Tristana_1.modify_command_line(1, 'Omnistomp')
    Tristana_1.modify_command_line(1, 'Skewer')
    Tristana_1.modify_command_line(1, 'Cyclotron')
    Tristana_1.modify_command_line(1, 'Speed')
    Tristana_1.modify_command_line(1, 'Omnistomp')
    Tristana_2 = deepcopy(Tristana_1)
    Tristana_2.turn(90)
    Tristana_2.name = 'Up'
    Tristana_3 = deepcopy(Tristana_2)
    Tristana_3.turn(90)
    Tristana_3.name = 'Left'
    Tristana_4 = deepcopy(Tristana_3)
    Tristana_4.turn(90)
    Tristana_4.name = 'Down'

    Tristanas: List[Mech] = [Tristana_1, Tristana_2, Tristana_3, Tristana_4]


    for Tristana in Tristanas:
        engine(Tristana.board, Tristana)
