import numpy as np
from abc import ABC, abstractmethod
from board import Board
from custom_types import Vector
from typing import Optional, List
from auxiliary_functions import tuple_to_vector, vector_to_tuple, oob_check, rotate, CustomError


class Entity(ABC):
    """Minion, mech, possibly bomb or boss even? Anything that can be placed on a board tile."""

    def __init__(self, board: Board, position: Vector, orientation: Vector, faction: str) -> None:
        """
        Creates an Entity (initializing the position and orientation), and places it onto the board.
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param orientation: Vector representing position change after a forward move, read custom_types.py for examples
        :param faction: Either the string 'Mechs' or 'Minions' representing allegiance
        """
        self.board = board
        self.position = position
        self.orientation = orientation
        self.faction = faction

        # checks if the specified position is within the game board
        if oob_check(self.board, self.position):
            # checks if the square already has something on it:
            if self.board[vector_to_tuple(position)].thing is not None:
                # if the square already has a friendly object on it, raise an Error
                # this will probably need to be changed later
                if self.board[vector_to_tuple(position)].thing.faction == 'Mechs':
                    raise CustomError("Yo this square already has a friendly object on it \
                    -- probably a Mech, Bomb or Wall")

            self.board[vector_to_tuple(self.position)].place_thing(self)



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


class Wall(Entity):
    """blocks stuff"""
    def __init__(self, board: Board, position: Vector, orientation: Optional[Vector] = None,
                 is_spiked: bool = False) -> None:
        """
        Creates a wall at the specified location (can have spikes in a specified direction)
        :param board: the Board object on which the wall is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param orientation: Vector representing position change after a forward move, read custom_types.py for examples.
        Also, this parameter is only needed if the wall is spiked, otherwise a default value is used.
        The orientation represents the direction that the spikes are facing in
        :param is_spiked: Boolean that indicates whether the wall is spiked or not
        """
        # this section of the code is to avoid mutable defaults
        if orientation is None:
            orientation = np.array([1, 0])
        else:
            orientation = np.array(orientation)  # Create a new array to avoid sharing

        # Walls will be friendly for now
        super().__init__(board, position, orientation, 'Mech')
        self.is_spiked = is_spiked

    def take_damage(self) -> None:
        """
        Have to implement this abstract method to please my IDE -- naturally, it doesn't do anything
        :return: None
        """
        pass


class Minion(Entity):
    def __init__(self, board: Board, position: Vector) -> None:
        """
        Creates a Minion (initializing the position), and places it onto the board. Minions don't have an orientation
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        """
        default_orientation = np.array([1, 0])  # filler
        super().__init__(board, position, default_orientation, 'Minions')

    def take_damage(self) -> None:
        """
        Minions die upon taking damage
        :return: None
        """
        self.board[vector_to_tuple(self.position)].remove_thing()


class Mech(Entity):
    def __init__(self, board: Board, position: Vector, orientation: Vector) -> None:
        """
        Creates the Mech (initializing the position and orientation), and places it onto the board.
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param orientation: Vector representing position change after a forward move, read custom_types.py for examples
        """
        super().__init__(board, position, orientation, 'Mechs')
        self.command_line: List = []

    def take_damage(self) -> None:
        """
        Draws a damage card -- this will be implemented much later
        :return: None
        """
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
        for i in range(1, level + 1):
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
