from __future__ import annotations
import numpy as np
from custom_types import Vector
from board import Board
from typing import TYPE_CHECKING, Callable

# This is for static type-checking
# Your IDE will interpret this as true, but it won't be true at run-time
# It's only for the type hints in Prompt.__init__()
if TYPE_CHECKING:
    from entities import Mech


def tuple_to_vector(input_tuple: tuple) -> Vector:
    """
    Converts a tuple into a 2x1 vector (shape (2, 1))
    :param input_tuple: tuple of length 2
    :return: 2x1 vector
    """
    return np.reshape(input_tuple, (2, 1))


def vector_to_tuple(input_vector: Vector) -> tuple:
    """Converts a 2x1 vector (shape (2,1)) into a tuple of length 2
    :param input_vector: 2x1 vector
    :return: tuple of length 2
    """
    return input_vector[(0, 0)], input_vector[(1, 0)]


def rotate(input_vector: Vector, angle: int) -> Vector:
    """
    Performs a linear transformation that rotates a 2x1 vector about the origin. Input only right angles.
    :param input_vector: 2x1 vector
    :param angle: -360, -270, -180, -90, 0, 90, 180, 270, or 360 (degrees)
    :return: 2x1 vector
    """
    if angle == 90 or angle == -270:
        rotation_matrix = np.array([[0, 1], [-1, 0]])
        return np.matmul(rotation_matrix, input_vector)
    elif angle == 180 or angle == -180:
        rotation_matrix = np.array([[-1, 0], [0, -1]])
        return np.matmul(rotation_matrix, input_vector)
    elif angle == 270 or angle == -90:
        rotation_matrix = np.array([0, -1], [1, 0])
        return np.matmul(rotation_matrix, input_vector)
    elif angle == 360 or angle == 0 or angle == -360:
        # literally don't rotate
        return input_vector


def oob_check(board: Board, location: Vector) -> bool:
    """
    Checks if a square exists on the board.
    :param board: the game board
    :param location: the coordinates of the square as a 2x1 column vector
    :return: True if the square exists, False if not
    """
    if location[0][0] < 0 or location[0][0] > len(board.board_array[0]) - 1:
        return False
    elif location[1][0] < 0 or location[1][0] > len(board.board_array[1]) - 1:
        return False
    else:
        return True


class Prompt:
    """Idk what I'm doing"""
    def __init__(self, num_options: int, executable: Callable[['Mech', int], None | Prompt]):
        """
        This class's sole purpose is to store functions that the engine/player can execute depending on a choice,
        either from the engine or the player
        :param num_options: the number of possible options
        :param executable: the function (probably with a match statement) that will accept an int
        (in the range of num_options) and act accordingly
        """
        self.num_options: int = num_options
        self.executable: Callable[['Mech', int], None | Prompt] = executable


class CustomError(Exception):
    """Used to raise an Error with whatever message you want"""
    def __init__(self, message="An error occurred - good luck"):
        self.message: str = message
        super().__init__(self.message)
