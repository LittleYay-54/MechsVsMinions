import numpy as np
from auxiliary_functions import vector_to_tuple, oob_check, Prompt
from typing import List
from custom_types import Matrix
from board import Board
from entities import Minion, Mech

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
                new_minion = Minion(board, coordinate)  # minions dont need an orientation
                # the minion should get placed if the square is empty (check Minion's initialization)


def initialize_starting_board(board: Board, minion_squares: Matrix, oil_squares: Matrix) -> None:
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


# this shouldn't be necessary anymore since instantiating Mechs already does this I think
# def place_player_mechs(board: Board, playing_mechs: List[Mech]) -> None:
#     """Place player mechs"""
#     for mech in playing_mechs:
#         board.players.append(mech)


# -- Gameplay --

# Turn structure is as follows:
# 1. Draft Command Cards, 2. Slot Command Cards, 3. Execute Command Lines
# 4. Minions Move, 5. Minions Spawn, 6. Minions Attack

def draft(board: Board):
    """Deal out Command Cards, let players pick Command Cards"""
    raise NotImplementedError


def slot_cards(board: Board):
    """Let players slot Command Cards"""
    raise NotImplementedError


def players_move(board: Board) -> None:
    """
    Players execute their command lines in order
    :return: None
    """
    # for player in board.players:
    #     execute_command_line(player)
    raise NotImplementedError


def rotate_hourglass(board: Board) -> None:
    """
    Shifts the order of the players by 1 upward, with the first player going to the back
    :return: None
    """
    board.players = board.players[1:] + board.players[:1]


def count_minions(board: Board) -> int:
    """
    Counts the minions currently on the board
    :return: the number of minions
    """
    count = 0
    for index, tile in np.ndenumerate(board.board_array):
        if tile.has_minion():
            count += 1
    return count
