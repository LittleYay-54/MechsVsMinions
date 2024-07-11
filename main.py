from engine import engine 
from basislists import generate
from board import Board
import numpy as np
if __name__ == '__main__':
    cards = ['b', 'c', 'f', 'o', 'o', 'sk', 'sp']
    commandline_lengths = [6]
    bases = generate(cards, commandline_lengths)
    board_space = np.array([0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0])
    board = Board(board_space)
    minion_squares = np.array([[[2, 0], [2, 1], [0, 2], [1, 2], [2, 4], [5, 2]]])
    oiled_squares = np.array([[2,2],[2,3],[3,2],[3,3]])
    board.spawn_minions(minion_squares)
    board.oil_squares(oiled_squares)
    position = np.array([0,0])
    engine(board, position, bases )



