import numpy as np
from types_1 import Vector
from board import Board

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
    if location[0][0] < 0 or location[0][0] > len(board[0]) - 1:
        return False
    elif location[1][0] < 0 or location[1][0] > len(board[1]) - 1:
        return False
    else:
        return True

def prompt(num_options: int) -> int:
    """
    This will handle "user choices" but more importantly engine logic.
    :param num_options: how many choices can be made here
    :return: an integer that represents the selected choice
    """
