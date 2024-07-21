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


players: List[Mech] = []


def place_player_mechs(board: Board, playing_mechs: List[Mech]) -> None:
    """Place player mechs"""
    for item in playing_mechs:
        players.append(item)


# -- Gameplay --

# Turn structure is as follows:
# 1. Draft Command Cards, 2. Slot Command Cards, 3. Execute Command Lines
# 4. Minions Move, 5. Minions Spawn, 6. Minions Attack

def draft():
    """Deal out Command Cards, let players pick Command Cards"""
    raise NotImplementedError


def slot_cards():
    """Let players slot Command Cards"""
    raise NotImplementedError


def players_move() -> None:
    """
    Players execute their command lines in order
    :return: None
    """
    def execute_command_line(player: Mech):
        for slot in range(1, 7):
            possible_prompt: Prompt | None = player.execute_command_card(slot)
            while isinstance(possible_prompt, Prompt):
                if possible_prompt.num_options == 1:
                    possible_prompt = possible_prompt.executable(player, 0)
                else:
                    # raise the input field
                    choice: int = int(input(f"Please select a choice (1-{possible_prompt.num_options}"))
                    possible_prompt = possible_prompt.executable(player, choice-1)

    for player in players:
        execute_command_line(player)


def rotate_hourglass() -> None:
    """
    Shifts the order of the players by 1 upward, with the first player going to the back
    :return: None
    """
    global players
    players: list[Mech] = players[1:] + players[:1]
