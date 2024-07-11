import numpy as np
from types import Vector, Matrix
from entities import Entity, Minion
from functions import tuple_to_vector, vector_to_tuple

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
        self.minion_count = 0 
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
            self.minion_count += 1 