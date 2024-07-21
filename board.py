import numpy as np
from numpy import ndarray, dtype
from numpy.typing import NDArray
from typing import TYPE_CHECKING, Tuple
from custom_types import NDArray2D

# This is for static type-checking
# Your IDE will interpret this as true, but it won't be true at run-time
# It's only for the type hints in Tile.place_thing()
if TYPE_CHECKING:
    from entities import Entity


class Tile:
    def __init__(self) -> None:
        """creates a Tile"""
        # In the future, it may be necessary for the Tiles to know their own location.
        # In this case, the __init__ for the Board class would also need to be modified
        # I'm leaving this here as a reminder:
        # self.location = location (obviously, add a new argument "location" to the function)
        self.oil: bool = False
        self.thing: Entity | None = None

    def spill_oil(self) -> None:
        """
        makes the Tile oiled
        :return: None
        """
        self.oil = True

    def place_thing(self, thing: 'Entity') -> None:
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

    def has_minion(self) -> bool:
        """
        checks if the Tile has a Minion on it
        :return: True if there's a Minion, false otherwise
        """
        if self.thing.faction == 'Minions':
            return True
        else:
            return False

    def has_friendly(self) -> bool:
        """
        checks if the Tile has a friendly Entity on it (i.e. Mech or Bomb)
        :return: True if there's a Mech or Bomb, false otherwise
        """
        if self.thing.faction == 'Mechs':
            return True
        else:
            return False

    def has_wall(self) -> bool:
        """
        checks if the Tile has a Wall on it
        :return: True if there's a Wall, false otherwise
        """
        if self.thing.faction == 'Neutral':
            return True
        else:
            return False

    def is_empty(self) -> bool:
        """
        checks if the Tile doesn't have any Entity on it
        :return: True if there's nothing on the Tile, false otherwise
        """
        if self.thing is None:
            return True
        else:
            return False


class Board:
    def __init__(self, boardspace: NDArray2D) -> None:
        """
        Creates a board object with the same shape as an input NDArray.
        :param boardspace: a 2D NDArray of the desired shape -- it doesn't matter what it actually contains
        """
        # makes new array full of new Tiles
        def create_tile(x, y):
            return Tile()

        # if the code is changed such that the Tiles know their own location, then use this function instead:
        # def create_tile(x, y):
        #     return Tile(x, y)

        vectorized_create_tile = np.vectorize(create_tile, otypes=[object])

        self.board_array: NDArray[Tile] = np.fromfunction(vectorized_create_tile, boardspace.shape, dtype=object)

    def __getitem__(self, index: Tuple[int, int]) -> Tile:
        """
        This dunder method allows you to index the board object directly
        :param index: a tuple of 2 ints, (x, y) coordinates
        :return: the Tile object that is stored at that position
        """
        # My IDE does not like the return type; it thinks it's an ndarray[Any, dtype[Tile]] instead of a Tile object
        # idk why
        return self.board_array[index]

