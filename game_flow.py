import numpy as np
from auxiliary_functions import vector_to_tuple, oob_check
from custom_types import Matrix
from board import Board
from entities import Minion

# This file is responsible for actually playing out the game by the rules


# -- Set-up --


def spawn_minions(board: Board, minion_squares: Matrix) -> None:
    """
    Spawns minions onto a specified list of squares of the board.
    :param board: the game board (Board)
    :param minion_squares: A Nx2 "Matrix", where the row "Vectors" represent coordinate pairs to spawn minions
    :return: None
    """
    coordinates = [minion_squares[i, :] for i in range(minion_squares.shape[0])]
    for coordinate in coordinates:
        # checks if the square is empty and within the board area
        if oob_check(board, coordinate):
            if board[vector_to_tuple(coordinate)].thing is None:
                new_minion = Minion(board, coordinate, np.array([1, 0]))  # filler orientation
                # the minion should get placed if the square is empty (check Minion's initialization)


def initialize_board(board: Board, minion_squares: Matrix, oil_squares: Matrix) -> None:
    """
    Spawns minions onto a specified list of squares of the board. Spills oil onto a specified list of squares of the board
    :param board: the game board (Board)
    :param minion_squares: A Nx2 "Matrix", where the row "Vectors" represent coordinate pairs to spawn minions
    :param oil_squares: A Nx2 "Matrix", where the row "Vectors" represent coordinate pairs to spill oil
    :return: None
    """
    spawn_minions(board, minion_squares)
    oil_coordinates = [oil_squares[i, :] for i in range(oil_squares.shape[0])]
    for oil_coordinate in oil_coordinates:
        # checks if the square is within the board area
        if oob_check(board, oil_coordinate):
            board[vector_to_tuple(oil_coordinate)].spill_oil()


# -- Gameplay --

