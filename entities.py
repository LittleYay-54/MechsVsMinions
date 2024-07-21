from __future__ import annotations
import numpy as np
from abc import ABC, abstractmethod
from board import Tile, Board
from custom_types import Vector
from typing import Optional, List, Dict, Tuple, Callable
from auxiliary_functions import vector_to_tuple, oob_check, rotate, Prompt, CustomError
from itertools import combinations, product


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

    def turn(self, angle: int) -> None:
        """
        Uses the rotate function from auxiliary_functions.py to change the Entity's orientation
        :param angle: a right angle in degrees, so like 90, -90, up to 360, -360
        :return: None
        """
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
                if self.board[vector_to_tuple(tentative_position)].is_empty():
                    # remove from current location, move to new location
                    self.raw_move(starting_position, tentative_position)
                else:
                    # if the space ahead has a Mech, then push it
                    if self.board[vector_to_tuple(tentative_position)].has_friendly():
                        # push the thing
                        self.board[vector_to_tuple(tentative_position)].thing.move(direction, 1)
                        # if it didn't get pushed into the edge, the space ahead should be empty, so move there
                        if self.board[vector_to_tuple(tentative_position)].is_empty():
                            # remove from current location, move to new location
                            self.raw_move(starting_position, tentative_position)
                    # if the space ahead has a Minion, then stomp it, and take damage
                    elif self.board[vector_to_tuple(tentative_position)].has_minion():
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
        self.health -= 1


class Mech(Entity):
    def __init__(self, board: Board, position: Vector, orientation: Vector) -> None:
        """
        Creates the Mech (initializing the position and orientation), and places it onto the board.
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param orientation: Vector representing position change after a forward move, read custom_types.py for examples
        """
        super().__init__(board, position, orientation, 'Mechs')
        self.command_line: List[List[str, int]] = [['Empty', 1], ['Empty', 1], ['Empty', 1],
                                                   ['Empty', 1], ['Empty', 1], ['Empty', 1]]

    card_colors: Dict[str, str] = {'Scythe': 'blue', 'Skewer': 'blue', 'Ripsaw': 'blue',
                                   'Fuel Tank': 'red', 'Blaze': 'red', 'Flamespitter': 'red',
                                   'Cyclotron': 'yellow', 'Speed': 'yellow', 'Chain Lightning': 'yellow',
                                   'Memory Core': 'green', 'Omnistomp': 'green', 'Hexmatic Aimbot': 'green',
                                   'Empty': 'none'}

    def modify_command_line(self, slot: int, card: str, level: int = 1) -> None:
        """
        Takes a card[level] (e.g. Blaze[2]) and attempts to place it in the desired slot.
        If no level is specified, it is assumed to be 1.
        Follows the rules of card stacking and overwriting; the result level cannot be greater than 3.
        :param slot: int from 1-6 representing location on the command line
        :param card: name of the card as a string (e.g. 'Blaze' or 'Omnistomp')
        :param level: int from 1-3 representing the level of the card you are trying to place
        (when you are placing multiple cards). If no level is given, it is assumed to be 1
        :return: None
        """
        if self.card_colors[self.command_line[slot - 1][0]] == self.card_colors[card]:
            new_level: int = self.command_line[slot - 1][1] + level
            if new_level > 3:
                new_level = 3
            self.command_line[slot - 1] = [card, new_level]
        else:
            self.command_line[slot - 1] = [card, level]

    def move(self, direction: Vector, num_squares: int) -> None:
        """
        Attempts to move the Mech in a certain direction a certain number of squares.
        Moving onto a Minion stomps the Minion. Pushing and towing logic is contained as well
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :return: None
        """
        remaining_moves: int = num_squares
        starting_position: Vector = self.position
        while remaining_moves > 0:
            tentative_position = self.position + direction
            if oob_check(self.board, tentative_position):
                # if the space is not occupied, just move
                if self.board[vector_to_tuple(tentative_position)].is_empty():
                    # remove from current location, move to new location
                    self.raw_move(starting_position, tentative_position)
                else:
                    # if the space ahead has a Mech or Bomb, then push it
                    if self.board[vector_to_tuple(tentative_position)].has_friendly():
                        # push the thing
                        self.board[vector_to_tuple(tentative_position)].thing.move(direction, 1)
                        # if it didn't get pushed into the edge, the space ahead should be empty, so move there
                        if self.board[vector_to_tuple(tentative_position)].is_empty():
                            # remove from current location, move to new location
                            self.raw_move(starting_position, tentative_position)
                    # if the space ahead has a Minion, then stomp it
                    elif self.board[vector_to_tuple(tentative_position)].has_minion():
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

    def scan(self, radius, faction) -> List[Vector]:
        """
        'Scans' around the mech in a certain radius to check for certain types of Entities
        (either Minions or friendly Entities). A radius of 1 means 1 square in any direction, including diagonals.
        :param radius: int representing searching distance
        :param faction: either 'Minions' or 'Mechs' to check for either Minions or friendly Entities
        :return: a list of Vectors that represent the positions of the objects found
        """
        squares: List[Vector] = []
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                if x != 0 or y != 0:
                    current_square: Vector = self.position + np.array([x, y])
                    if oob_check(self.board, current_square):
                        if faction == 'Minions':
                            if self.board[vector_to_tuple(current_square)].has_minion():
                                squares.append(current_square)
                        elif faction == 'Mechs':
                            if self.board[vector_to_tuple(current_square)].has_friendly():
                                squares.append(current_square)
        return squares

    def blaze(self, level: int) -> Prompt:
        def executable(mech: Mech, choice: int) -> None:
            mech.move(mech.orientation, level)
            mech.damage(mech.position + rotate(mech.orientation, -90))
            mech.damage(mech.position + rotate(mech.orientation, 90))
        prompt = Prompt(1, executable)
        return prompt

    def fuel_tank(self, level: int) -> Prompt:
        def executable(mech: Mech, choice: int) -> None:
            match choice:
                case 0:
                    mech.turn(90)
                case 1:
                    mech.turn(-90)
                case 2:
                    mech.turn(180)
                case 3:
                    mech.turn(0)
        prompt = Prompt(level+1, executable)
        return prompt

    def flamespitter(self, level: int) -> Prompt:
        target_squares: List[Vector] = []
        pointer: Vector = self.orientation.copy()
        target_squares.append(pointer.copy())
        pointer += self.orientation
        target_squares.append(pointer.copy())
        if level >= 2:
            target_squares.append(pointer + rotate(self.orientation, -90))
            target_squares.append(pointer + rotate(self.orientation, 90))
            if level == 3:
                pointer += self.orientation
                target_squares.append(pointer.copy())
                target_squares.append(pointer + rotate(self.orientation, -90))
                target_squares.append(pointer + rotate(self.orientation, 90))

        def executable(mech: Mech, choice: int) -> None:
            for square in target_squares:
                self.damage(square)
        prompt = Prompt(1, executable)
        return prompt

    def speed(self, level: int) -> Prompt:
        def executable(choice: int) -> None:
            match choice:
                case 0:
                    self.move(self.orientation, level)
                case 1:
                    self.move(self.orientation, level+1)
                case 2:
                    self.move(self.orientation, level+2)
                case 3:
                    self.move(self.orientation, level+3)
        prompt = Prompt(level+1, executable)
        return prompt

    def cyclotron(self, level: int) -> Prompt:
        def executable(choice: int) -> None:
            for i in range(1, level + 1):
                self.damage(self.position + np.array([i, i]))
                self.damage(self.position + np.array([-i, i]))
                self.damage(self.position + np.array([i, -i]))
                self.damage(self.position + np.array([-i, -i]))
            match choice:
                case 0:
                    self.turn(90)
                case 1:
                    self.turn(-90)
                case 2:
                    self.turn(180)
                case 3:
                    self.turn(0)
        prompt = Prompt(level + 1, executable)
        return prompt

    def chain_lightning(self, level: int) -> Prompt:
        raise NotImplementedError
        squares_in_front: List[Vector] = [
            self.position + self.orientation,
            self.position + self.orientation + rotate(self.orientation, 90),
            self.position + self.orientation + rotate(self.orientation, -90)
        ]
        chains_left = level*2 - 1

        def executable(choice: int) -> Prompt:
            # search diagonals
            diagonals: List[Vector] = [
                self.position + np.array(point) for point in product((-1, 1), (-1, 1))
            ]
            can_chain = False
            for diagonal_square in diagonals:
                if oob_check(self.board, diagonal_square):
                    if self.board[vector_to_tuple(diagonal_square)].has_minion():
                        can_chain = True
        prompt = Prompt(0, executable)
        return prompt

    def skewer(self, level: int) -> Prompt:
        def execute(choice: int) -> None:
            self.move(self.orientation, level)
        prompt = Prompt(1, execute)
        return prompt

    def scythe(self, level: int) -> Prompt:
        viable_squares: List[Vector] = self.scan(1, 'Minions')
        damage_combinations: List[tuple[Vector]] = list(combinations(viable_squares, level))
        if len(viable_squares) < level:
            damage_combinations = [tuple(viable_squares)]
        num_damage_combinations: int = len(damage_combinations)

        def executable(choice: int) -> None:
            chosen_strike, turn_angle = divmod(num_damage_combinations, choice)
            targeted_squares: Tuple[Vector] = damage_combinations[chosen_strike]
            for square in targeted_squares:
                self.damage(square)
            match choice:
                case 0:
                    self.turn(90)
                case 1:
                    self.turn(-90)
                case 2:
                    self.turn(180)
                case 3:
                    self.turn(0)
        prompt = Prompt(num_damage_combinations * (level + 1), executable)
        return prompt

    def ripsaw(self, level: int) -> Prompt:
        # scan for the targets
        target_squares: List[Vector] = []
        pointer: Vector = self.position + self.orientation
        ripsaws_left = level
        while oob_check(self.board, pointer) and ripsaws_left > 0:
            curr_square: Tile = self.board[vector_to_tuple(pointer)]
            if curr_square.has_friendly() or curr_square.has_wall():
                break
            elif curr_square.has_minion():
                target_squares.append(pointer.copy())
                ripsaws_left -= 1
            pointer += self.orientation

        def executable(choice: int) -> None:
            for square in target_squares:
                self.damage(square)
        prompt = Prompt(1, executable)
        return prompt

    def omnistomp(self, level: int) -> Prompt:
        def executable(choice: int) -> None:
            match choice:
                case 0:
                    self.move(rotate(self.orientation, -90), level)
                case 1:
                    self.move(self.orientation, level)
                case 2:
                    self.move(rotate(self.orientation, 90), level)
        prompt = Prompt(3, executable)
        return prompt

    def memory_core(self, level: int) -> Prompt:
        def executable(choice: int) -> None:
            match choice:
                case 0:
                    self.turn(90)
                case 1:
                    self.turn(-90)
                case 2:
                    self.turn(180)
                case 3:
                    self.turn(0)
        prompt = Prompt(level + 1, executable)
        return prompt

    def hexmatic_aimbot(self, level: int) -> Prompt:
        # scan for targets
        target_squares: List[Vector] = self.scan(3, 'Minions')

        def executable(choice: int) -> None:
            self.damage(target_squares[choice])
        prompt = Prompt(len(target_squares), executable)
        return prompt

    translations: Dict[str, Callable[[Mech, int], Prompt | None]] = {
        'Scythe': scythe, 'Skewer': skewer, 'Ripsaw': ripsaw,
        'Fuel Tank': fuel_tank, 'Blaze': blaze, 'Flamespitter': flamespitter,
        'Cyclotron': cyclotron, 'Speed': speed, 'Chain Lightning': chain_lightning,
        'Memory Core': memory_core, 'Omnistomp': omnistomp, 'Hexmatic Aimbot': hexmatic_aimbot
    }

    def execute_command_card(self, slot: int) -> Prompt | None:
        command_card_string = self.command_line[slot-1][0]
        command_card_level = self.command_line[slot-1][1]
        command_card_method = self.translations[command_card_string]
        return command_card_method(self, command_card_level)
