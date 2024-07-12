import numpy as np
from typing import Tuple
from custom_types import Vector, Matrix, NDArray2D
from entities import Entity, Minion
from auxiliary_functions import tuple_to_vector, vector_to_tuple


class Tile:
    def __init__(self) -> None:
        """creates a Tile"""
        # In the future, it may be necessary for the Tiles to know their own location.
        # In this case, the __init__ for the Board class would also need to be modified
        # I'm leaving this here as a reminder:
        # self.location = location (obviously, add a new argument "location" to the function)
        self.oil = False
        self.thing = None

    def spill_oil(self) -> None:
        """
        makes the Tile oiled
        :return: None
        """
        self.oil = True

    def place_thing(self, thing: Entity) -> None:
        """
        places an Entity on the tile
        :param thing: an Entity
        :return: None
        """
        self.thing = thing

    def remove_thing(self) -> None:
        """
        clears the Tile of any Entities
        :return: None
        """
        self.thing = None

class Board:
    def __init__(self, boardspace: NDArray2D) -> None:
        """
        Creates a board object with the same shape as an input NDArray.
        :param boardspace: a 2D NDArray of the desired shape -- it doesn't matter what it actually contains
        """
        self.board = np.empty(boardspace.shape, dtype=Tile)
        for index in np.ndindex(self.board.shape):
            self.board[index] = Tile()

    def __getitem__(self, index: Tuple[int, int]) -> Tile:

        return self.board[index]

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