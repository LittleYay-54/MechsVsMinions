import numpy as np
import itertools
from abc import ABC, abstractmethod

# typing that I will use to represent 2x1 vectors of ints
Vector = np._typing.NDArray[np.int_]
# typing that I will use to represent 2xn "matrices" of data that really just store multiple vectors
Matrix = np._typing.NDArray[np.int_]
# they are literally the same but idc


def tuple_to_vector(input_tuple: tuple) -> Vector:
    """
    Converts a tuple into a 2x1 vector (literally shape (2,1), not (2))
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
    :param angle: -360, -270, -180, -90, 0, 90, 180, 270, or 360
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
        pass


class Tile:
    def __init__(self, location: Vector) -> None:
        self.location = location
        self.oil = False
        self.thing = None

    def spill_oil(self) -> None:
        self.oil = True

    def place_thing(self, thing: Entity) -> None:
        self.thing = thing

    def remove_thing(self) -> None:
        self.thing = None

class Board:
    def __init__(self, boardspace: np._typing.NDArray) -> None:
        """
        Creates a board object with the same shape as the shape of an input NDArray
        :param boardspace: a 2D NDArray -- it doesn't matter what it contains
        """
        self.board = np.empty(boardspace.shape, dtype=Tile)
        for index in np.ndindex(self.board.shape):
            self.board[index] = Tile(tuple_to_vector(index))

    def oil_squares(self, oiled_squares: Matrix) -> None:
        """
        Places oil on specified squares of the board. The coordinates of the squares should be a matrix where
        the column vectors represent square locations.
        :param oiled_squares: A 2xN NDArray "Matrix"
        :return: None
        """
        coordinates = [oiled_squares[:, i][:, np.newaxis] for i in range(oiled_squares.shape[1])]
        for coordinate in coordinates:
            self.board[vector_to_tuple(coordinate)].spill_oil()

    def spawn_minions(self, minion_squares: Matrix) -> None:
        """
        Spawns minions on specified squares of the board. The coordinates of the squares should be a matrix where
        the column vectors represent square locations.
        :param minion_squares: a 2xN NDArray "Matrix"
        :return: None
        """
        coordinates = [minion_squares[:, i][:, np.newaxis] for i in range(minion_squares.shape[1])]
        for coordinate in coordinates:
            new_minion = Minion(coordinate, np.array([[1], [0]]))
            self.board[vector_to_tuple(coordinate)].place_thing(new_minion)


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


class Entity(ABC):
    """Minion, mech, possibly bomb or boss even?"""
    def __init__(self, board: Board, position: Vector, orientation: Vector) -> None:
        """Position should be a 2x1 vector.
        Orientation should also be a 2x1 vector such that
        a forward move "adds" the orientation to the position.
        i.e, position could be [[1], [2]], and an orientation of [[0], [-1]] would indicate
        "downward facing" and a forward move would change the position to [[1], [1]]"""
        self.board = board
        self.position = position
        self.orientation = orientation

    def move(self, direction: Vector) -> None:
        tentative_position = self.position + direction
        if oob_check(tentative_position):
            self.board[vector_to_tuple(self.position)].remove_thing()
            # this next line will delete minions when they are "stomped on";
            # it needs to be rewritten in the future so that minions can't stomp things
            # and it's not possible for mechs, bombs, etc. to be deleted via getting "stomped on"
            self.board[vector_to_tuple(tentative_position)].place_thing(self)
            self.position = tentative_position

    def turn(self, angle: int) -> None:
        """Uses the rotate function from the global scope to change orientation"""
        self.orientation = rotate(self.orientation, angle)

    def damage(self, target_square: Vector) -> None:
        if oob_check(self.board, target_square):
            self.board[vector_to_tuple(target_square)].thing.take_damage()

    @abstractmethod
    def take_damage(self):
        "specify how different entities take damage (minions, mechs, boss, bomb)"
        pass


class Minion(Entity):
    def __init__(self, board: Board, position: Vector, orientation: Vector) -> None:
        super().__init__(board, position, orientation)

    def take_damage(self) -> None:
        "minions die upon taking damage"
        self.board[vector_to_tuple(self.position)].remove_thing()



class Mech(Entity):
    def __init__(self, board: Board, position: Vector, orientation: Vector, command_line: list) -> None:
        super().__init__(board, position, orientation)
        self.command_line = command_line

    def take_damage(self) -> None:
        # this will be implemented much later
        pass

    def blaze(self, level: int) -> None:
        for i in range(level):
            self.move(self.orientation)
        self.damage(self.position + rotate(self.orientation, -90))
        self.damage(self.position + rotate(self.orientation, 90))

    def fuel_tank(self, level: int) -> None:
        pass

    def flamespitter(self, level: int) -> None:
        pointer = self.orientation.copy()
        self.damage(pointer)
        pointer += self.orientation
        self.damage(pointer)
        if level >= 2:
            self.damage(pointer + rotate(self.orientation, -90))
            self.damage(pointer + rotate(self.orientation, 90))
            if level == 3:
                pointer += self.orientation
                self.damage(pointer)
                self.damage(pointer + rotate(self.orientation, -90))
                self.damage(pointer + rotate(self.orientation, 90))

    def speed(self, level: int) -> None:
        pass

    def cyclotron(self, level: int) -> None:
        for i in range(1, level+1):
            self.damage(self.position + [[i], [i]])
            self.damage(self.position + [[-i], [i]])
            self.damage(self.position + [[i], [-i]])
            self.damage(self.position + [[-i], [-i]])

        # turn functionality

    def chain_lightning(self, level: int) -> None:
        pass

    def skewer(self, level: int) -> None:
        for i in range(level):
            self.move(self.orientation)

    def scythe(self, level: int) -> None:
        pass

    def ripsaw(self, level: int) -> None:
        pass

    def omnistomp(self, level: int) -> None:
        pass

    def memory_core(self, level: int) -> None:
        pass

    def hexmatic_aimbot(self, level: int) -> None:
        pass


# TIME TO MAKE THE ENGINE
engine = None



