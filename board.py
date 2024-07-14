import numpy as np
from numpy.typing import NDArray
from typing import Tuple
from custom_types import NDArray2D
from entities import Entity


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

        self.board_array: NDArray[Tile] = vectorized_create_tile(*np.indices(boardspace.shape))

        # def create_tile(x, y):
        #     return Tile(x, y)  # Assuming Tile constructor accepts position
        #
        # vectorized_create_tile = np.vectorize(create_tile, otypes=[object])
        #
        # indices = np.indices(boardspace.shape)
        # self.board_array = vectorized_create_tile(indices[0], indices[1])

    def __getitem__(self, index: Tuple[int, int]) -> Tile:
        """
        This dunder method allows you to index the board object directly
        :param index: a tuple of 2 ints, (x, y) coordinates
        :return: the Tile object that is stored at that position
        """
        # My IDE does not like the return type; it thinks it's an ndarray[Any, dtype[Tile]] instead of a Tile object
        # idk why
        return self.board_array[index]

