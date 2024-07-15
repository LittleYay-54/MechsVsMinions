import numpy as np
from abc import ABC, abstractmethod
from board import Board
from custom_types import Vector
from typing import Optional, List
from auxiliary_functions import vector_to_tuple, oob_check, rotate, CustomError


class Entity(ABC):
    """Minion, mech, possibly bomb or boss even? Anything that can be placed on a board tile."""

    def __init__(self, board: Board, position: Vector, orientation: Vector, faction: str) -> None:
        """
        Creates an Entity (initializing the position and orientation), and places it onto the board.
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param orientation: Vector representing position change after a forward move, read custom_types.py for examples
        :param faction: Either the string 'Mechs', 'Minions', or 'Neutral' representing allegiance
        """
        self.board: Board = board
        self.position: Vector = position
        self.orientation: Vector = orientation
        self.faction: str = faction

        # checks if the specified position is within the game board
        if oob_check(self.board, self.position):
            # if the square is empty, then place the object
            if self.board[vector_to_tuple(position)].thing is None:
                self.board[vector_to_tuple(self.position)].place_thing(self)
            # if the square already has an object on it
            else:
                # if the square contains a Minion, simply replace the minion
                if self.board[vector_to_tuple(position)].thing.faction == 'Minions':
                    self.board[vector_to_tuple(self.position)].place_thing(self)
                # if it has a friendly object, then raise an error
                # this probably needs to be changed later
                if self.board[vector_to_tuple(position)].thing.faction == 'Mechs':
                    raise CustomError("Yo this square already has a friendly object on it \
                    -- probably a Mech, Bomb or Wall")

    def raw_move(self, starting_position, ending_position) -> None:
        """
        Removes an Entity from its current position and moves it to a new one. For use in the actual move methods.
        :param starting_position: Vector representing where the Entity began
        :param ending_position: Vector representing where the Entity ends up
        :return: None
        """
        self.board[vector_to_tuple(starting_position)].remove_thing()
        self.board[vector_to_tuple(ending_position)].place_thing(self)
        self.position = ending_position

    @abstractmethod
    def move(self, direction: Vector, num_squares: int) -> None:
        """
        Entities (really just Mechs, the Bomb, Minions, and the Boss) can move
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :return: None
        """
        remaining_moves = num_squares
        while remaining_moves > 0:
            starting_position = self.position
            tentative_position = self.position + direction
            if oob_check(self.board, tentative_position):
                # if the space is not occupied, just move
                if self.board[vector_to_tuple(tentative_position)].thing is None:
                    # remove from current location, move to new location
                    self.raw_move(starting_position, tentative_position)
                else:
                    # if the space is occupied and the moving object is a Minion, then look for another direction
                    if self.faction == 'Minions':
                        # search for another direction to move in
                        pass
                    # if space is occupied by a friendly object and the moving object is a Mech, then push
                    elif self.board[vector_to_tuple(tentative_position)].thing.faction == 'Mechs':
                        # push the thing
                        self.board[vector_to_tuple(tentative_position)].thing.move(direction, 1)
                        # if it didn't get pushed into the edge, the space ahead should be empty, so move there
                        if self.board[vector_to_tuple(tentative_position)].thing is None:
                            self.raw_move(starting_position, tentative_position)
                    # if the space is occupied by a Minion and the moving object is a Mech, then stomp it
                    elif self.board[vector_to_tuple(tentative_position)].thing.faction == 'Minions':
                        # kill the minion


            # towing
            # if the moving object is a Mech and they have enough moves, allow a towing option
            # scan for nearby towable objects around starting position
            # if remaining_moves >= 2,
            # prompt if you want towing or not
            # decrement remaining_moves if towing was chosen

            remaining_moves -= 1


    def turn(self, angle: int) -> None:
        """Uses the rotate function from auxiliary_functions.py to change orientation"""
        self.orientation = rotate(self.orientation, angle)

    def damage(self, target_square: Vector) -> None:
        if oob_check(self.board, target_square):
            if self.faction != self.board[vector_to_tuple(target_square)].thing.faction:
                self.board[vector_to_tuple(target_square)].thing.take_damage()

    @abstractmethod
    def take_damage(self):
        """specify how different entities take damage (minions, mechs, boss, bomb)"""
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

        super().__init__(board, position, orientation, 'Neutral')
        self.is_spiked = is_spiked

    def move(self, direction: Vector, num_squares: int) -> None:
        """
        Have to implement this abstract method -- Walls can't move
        :return: None
        """
        pass

    def take_damage(self) -> None:
        """
        Have to implement this abstract method -- Walls don't take damage
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

    def move(self, direction: Vector, num_squares: int) -> None:
        """
        Attempts to move the Minion a certain number of squares in a certain direction.
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :return: None
        """
        remaining_moves = num_squares
        while remaining_moves > 0:
            starting_position = self.position
            tentative_position = self.position + direction
            if oob_check(self.board, tentative_position):
                # if the space is not occupied, just move
                if self.board[vector_to_tuple(tentative_position)].thing is None:
                    # remove from current location, move to new location
                    self.raw_move(starting_position, tentative_position)
                else:
                    # search for another direction to move in (thus a new tentative position)
                    # figure this out later
                    pass
            remaining_moves -= 1


    def take_damage(self) -> None:
        """
        Minions die upon taking damage
        :return: None
        """
        self.board[vector_to_tuple(self.position)].remove_thing()

class Bomb(Entity):
    """the Bomb -- has HP; is friendly but doesn't do much"""
    def __init__(self, board: Board, position: Vector, health: int) -> None:
        """
        Creates the Bomb (initializing position), gives it an amount of HP, and places it on the board.
        Orientation doesn't matter.
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param health: amount of HP the bomb starts with
        """
        default_orientation = np.array([1, 0])  # filler
        super().__init__(board, position, default_orientation, 'Mechs')
        self.health: int = health

    def move(self, direction: Vector, num_squares: int) -> None:
        """
        Attempts to move the Bomb in a direction a certain number of squares.
        This only occurs due to a Mech pushing or towing it.
        If the bomb tries to move onto a Minion, it stomps the Minion, killing it, but also taking 1 damage.
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :return: None
        """
        remaining_moves = num_squares
        starting_position = self.position
        while remaining_moves > 0:
            tentative_position = self.position + direction
            if oob_check(self.board, tentative_position):
                # if the space is not occupied, just move
                if self.board[vector_to_tuple(tentative_position)].thing is None:
                    # remove from current location, move to new location
                    self.raw_move(starting_position, tentative_position)
                else:
                    # if the space ahead has a Mech, then push it
                    if self.board[vector_to_tuple(tentative_position)].thing.faction == 'Mechs':
                        # push the thing
                        self.board[vector_to_tuple(tentative_position)].thing.move(direction, 1)
                        # if it didn't get pushed into the edge, the space ahead should be empty, so move there
                        if self.board[vector_to_tuple(tentative_position)].thing is None:
                            # remove from current location, move to new location
                            self.raw_move(starting_position, tentative_position)
                    # if the space ahead has a Minion, then stomp it, and take damage
                    elif self.board[vector_to_tuple(tentative_position)].thing.faction == 'Minions':
                        # kill the minion
                        self.board[vector_to_tuple(tentative_position)].thing.take_damage()
                        # take damage
                        self.take_damage()
                        # move there
                        self.raw_move(starting_position, tentative_position)
            remaining_moves -= 1

    def take_damage(self) -> None:
        """
        When the Bomb takes damage, it loses 1 HP
        :return: None
        """

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

    def move(self, direction: Vector, num_squares: int) -> None:
        """
        Attempts to move the Mech in a certain direction a certain number of squares.
        Moving onto a Minion stomps the Minion. Pushing and towing logic is contained as well
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :return: None
        """
        remaining_moves = num_squares
        starting_position = self.position
        while remaining_moves > 0:
            tentative_position = self.position + direction
            if oob_check(self.board, tentative_position):
                # if the space is not occupied, just move
                if self.board[vector_to_tuple(tentative_position)].thing is None:
                    # remove from current location, move to new location
                    self.raw_move(starting_position, tentative_position)
                else:
                    # if the space ahead has a Mech or Bomb, then push it
                    if self.board[vector_to_tuple(tentative_position)].thing.faction == 'Mechs':
                        # push the thing
                        self.board[vector_to_tuple(tentative_position)].thing.move(direction, 1)
                        # if it didn't get pushed into the edge, the space ahead should be empty, so move there
                        if self.board[vector_to_tuple(tentative_position)].thing is None:
                            # remove from current location, move to new location
                            self.raw_move(starting_position, tentative_position)
                    # if the space ahead has a Minion, then stomp it, and take damage
                    elif self.board[vector_to_tuple(tentative_position)].thing.faction == 'Minions':
                        # kill the minion
                        self.board[vector_to_tuple(tentative_position)].thing.take_damage()
                        # move there
                        self.raw_move(starting_position, tentative_position)
            remaining_moves -= 1

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
