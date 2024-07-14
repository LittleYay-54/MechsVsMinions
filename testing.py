import numpy as np

new_array = np.array([1, 2])
print(new_array.shape)
print(new_array.shape == (2))
print(new_array.shape == (2,))

# ok I'm confused


from typing import NewType, Annotated
greeting = Annotated[str, "Welcome Message"]
a: greeting = "Hello"
print(greeting)


import numpy as np
from numpy.typing import NDArray
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
        # I don't understand what this following code does:
        def create_tile():
            return Tile()

        vectorized_create_tile = np.vectorize(create_tile, otypes=[object])

        self.board: NDArray[Tile] = vectorized_create_tile(*np.indices(boardspace.shape))

        # def create_tile(x, y):
        #     return Tile(x, y)  # Assuming Tile constructor accepts position
        #
        # vectorized_create_tile = np.vectorize(create_tile, otypes=[object])
        #
        # indices = np.indices(boardspace.shape)
        # self.board = vectorized_create_tile(indices[0], indices[1])

    def __getitem__(self, index: Tuple[int, int]) -> Tile:
        """
        This dunder method allows you to index the board directly
        :param index: a tuple of 2 ints, (x, y) coordinates
        :return: the Tile object that is stored at that position
        """
        return self.board[index]

    def oil_squares(self, oiled_squares: Matrix) -> None:
        """
        Spills oil upon a specified list of squares on the board.
        :param oiled_squares: A Nx2 "Matrix", where the row "Vectors" represent coordinate pairs
        :return: None
        """
        coordinates = [oiled_squares[i, :] for i in range(oiled_squares.shape[0])]
        for coordinate in coordinates:
            self.board[vector_to_tuple(coordinate)].spill_oil()

    def spawn_minions(self, minion_squares: Matrix) -> None:
        """
        Spawns minions on a specified list of squares of the board.
        :param minion_squares: A Nx2 "Matrix", where the row "Vectors" represent coordinate pairs
        :return: None
        """
        coordinates = [minion_squares[i, :] for i in range(minion_squares.shape[0])]
        for coordinate in coordinates:
            new_minion = Minion(self, coordinate, np.array([1, 0]))  # filler orientation
            self.board[vector_to_tuple(coordinate)].place_thing(new_minion)


example_boardspace: NDArray = np.zeros((6, 6))
myboard: Board = Board(example_boardspace)

