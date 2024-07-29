from __future__ import annotations
import numpy as np
from abc import ABC, abstractmethod
from board import Tile, Board
from custom_types import Vector
from typing import Optional, List, Dict, Callable, Tuple
from auxiliary_functions import vector_to_tuple, oob_check, rotate, Prompt, CustomError
from itertools import combinations, product
from functools import partial


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
    def move(self, direction: Vector, num_squares: int, pushed: Optional[Entity] = None) -> None:
        """
        Entities (really just Mechs, the Bomb, Minions, and the Boss) can move
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :param pushed: indicates if this movement was due to pushing -- input the Entity which did the pushing if so
        :return: None
        """
        ...

    def turn(self, angle: int) -> None:
        """
        Uses the rotate function from auxiliary_functions.py to change the Entity's orientation
        :param angle: a right angle in degrees, so like 90, -90, up to 360, -360
        :return: None
        """
        self.orientation = rotate(self.orientation, angle)

    def damage(self, target_square: Vector) -> None:
        """
        An Entity inflicts damage onto another Entity if they are not part of the same faction.
        :param target_square: the square (as a Vector) that the damaging Entity is targeting
        :return: None
        """
        if oob_check(self.board, target_square):
            if self.faction != self.board[vector_to_tuple(target_square)].thing.faction:
                self.board[vector_to_tuple(target_square)].thing.take_damage()

    def damage_multiple(self, target_squares: List[Vector]) -> None:
        """
        An Entity attempts to damage multiple squares at once (causing Entities on these squares to take damage
        if they are not part of the same faction
        :param target_squares: the list of squares (Vectors) that the damaging Entity is targeting
        :return: None
        """
        for square in target_squares:
            self.damage(square)

    @abstractmethod
    def take_damage(self):
        """specify how different entities take damage (Minions, Mechs, Boss, Bomb)"""
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

        super().__init__(board, position, orientation, 'Neutral')
        self.is_spiked = is_spiked

    def move(self, direction: Vector, num_squares: int, pushed: Optional[Entity] = False) -> None:
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

    def move(self, direction: Vector, num_squares: int, pushed: Optional[Entity] = None) -> None:
        """
        Attempts to move the Minion a certain number of squares in a certain direction.
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :param pushed: as far as I know, Minions can't be pushed, so this shouldn't be relevant
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


class Friendly(Entity):
    """Friendly Entities -- i.e., Mechs and the Bomb"""
    def __init__(self, board: Board, position: Vector, orientation: Vector, is_bomb: bool) -> None:
        """is_bomb makes the Entity take damage upon stomping bombs"""
        super().__init__(board, position, orientation, 'Mechs')
        self.is_bomb: bool = is_bomb

    @abstractmethod
    def move(self, direction: Vector, num_squares: int, pushed: Optional[Entity] = None) -> None:
        """Implement separately for Mechs and the Bomb"""
        pass

    @abstractmethod
    def take_damage(self):
        """Implement separately for Mechs and the Bomb"""
        pass

    def can_move(self, curr_square: Vector, direction: Vector) -> bool:
        """Checks if a move wouldn't be obstructed"""
        next_square: Vector = curr_square + direction
        if oob_check(self.board, next_square):
            if self.board[vector_to_tuple(next_square)].has_wall():
                return False
            # if there is a friendly Entity blocking, check if it can be pushed via recursion
            if self.board[vector_to_tuple(next_square)].has_friendly():
                return self.can_move(next_square, direction)
            else:
                return True
        else:
            return False

    def movement_logic(self, direction: Vector) -> bool:
        """The main reason for this subclass -- this method just moves the object 1 square in a direction,
        accounting for Minion stomping and pushing. Returns True if the object successfully moved, False if it couldn't"""
        starting_position: Vector = self.position.copy()
        tentative_position: Vector = self.position + direction
        if self.can_move(starting_position, direction):
            # if the space is not occupied, just move
            if self.board[vector_to_tuple(tentative_position)].is_empty():
                # remove from current location, move to new location
                self.raw_move(starting_position, tentative_position)
            # if the space ahead has a Mech, then push it
            elif self.board[vector_to_tuple(tentative_position)].has_friendly():
                # push the thing
                self.board[vector_to_tuple(tentative_position)].thing.move(direction, 1, self)
                # remove from current location, move to new location
                self.raw_move(starting_position, tentative_position)
                # blocking is already dealt with via self.can_move()
            # if the space ahead has a Minion, then stomp it, and take damage if the Entity is a Bomb
            elif self.board[vector_to_tuple(tentative_position)].has_minion():
                # kill the minion
                self.board[vector_to_tuple(tentative_position)].thing.take_damage()
                # take damage if the Entity is a Bomb
                if self.is_bomb:
                    self.take_damage()
                # move there
                self.raw_move(starting_position, tentative_position)

            # if successfully moved and now on oil, attempt to move again
            if self.board[vector_to_tuple(self.position)].is_oiled():
                self.movement_logic(direction)

            return True

        else:
            return False


class Bomb(Friendly):
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
        super().__init__(board, position, default_orientation, True)
        self.health: int = health

    def move(self, direction: Vector, num_squares: int, pushed: Optional[Entity] = None) -> None:
        """
        Attempts to move the Bomb in a direction a certain number of squares.
        This only occurs due to a Mech pushing it (not towing it).
        If the bomb tries to move onto a Minion, it stomps the Minion, killing it, but also taking 1 damage.
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :param pushed: If the movement was due to pushing, input the Entity which did the pushing, otherwise, input nothing
        :return: None
        """
        remaining_moves: int = num_squares
        while remaining_moves > 0:
            successfully_moved: bool = self.movement_logic(direction)
            if not successfully_moved:
                break
            remaining_moves -= 1

    def take_damage(self) -> None:
        """
        When the Bomb takes damage, it loses 1 HP
        :return: None
        """
        self.health -= 1


class Mech(Friendly):
    def __init__(self, board: Board, position: Vector, orientation: Vector, name: str) -> None:
        """
        Creates the Mech (initializing the position and orientation), and places it onto the board.
        :param board: the Board object on which the object is placed on
        :param position: Vector representing (x,y) coordinates, except 0-indexed
        :param orientation: Vector representing position change after a forward move, read custom_types.py for examples
        """
        super().__init__(board, position, orientation, False)
        self.name: str = name
        self.command_line: List[Tuple[str, int]] = [
            ('Empty', 1),
            ('Empty', 1),
            ('Empty', 1),
            ('Empty', 1),
            ('Empty', 1),
            ('Empty', 1)
        ]
        self.prompt_stack: List[Prompt] = []
        self.board.players.append(self)

    def stack_push(self, prompt):
        """Pushes a prompt object to the top of the Mech's prompt stack"""
        self.prompt_stack.append(prompt)

    card_colors: Dict[str, str] = {
        'Scythe': 'blue', 'Skewer': 'blue', 'Ripsaw': 'blue',
        'Fuel Tank': 'red', 'Blaze': 'red', 'Flamespitter': 'red',
        'Cyclotron': 'yellow', 'Speed': 'yellow', 'Chain Lightning': 'yellow',
        'Memory Core': 'green', 'Omnistomp': 'green', 'Hexmatic Aimbot': 'green',
        'Empty': 'none'
    }

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
            self.command_line[slot - 1] = (card, new_level)
        else:
            self.command_line[slot - 1] = (card, level)

    def scan(self, radius: int, faction: str, towing: Optional[Vector] = None) -> List[Vector]:
        """
        'Scans' around the mech in a certain radius to check for certain types of Entities
        (either Minions or friendly Entities). A radius of 1 means 1 square in any direction, including diagonals.
        :param radius: int representing searching distance
        :param faction: either 'Minions' or 'Mechs' to check for either Minions or friendly Entities
        :param towing: Only use if the scan is being used to scan for towable objects. The default is None,
        in which case, all squares (including diagonals) are checked. If a Vector is given
        (the location to which the towing object is moving), then diagonals will not be checked,
        and the towing direction will also not be checked
        :return: a list of Vectors that represent the positions of the objects found
        """
        squares: List[Vector] = []
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if x != 0 or y != 0:
                    if towing is not None:
                        if x != 0 and y != 0:
                            break
                        elif x == towing[0] and y == towing[1]:
                            break
                    current_square: Vector = self.position + np.array([x, y])
                    if oob_check(self.board, current_square):
                        if faction == 'Minions':
                            if self.board[vector_to_tuple(current_square)].has_minion():
                                squares.append(current_square)
                        elif faction == 'Mechs':
                            if self.board[vector_to_tuple(current_square)].has_friendly():
                                squares.append(current_square)
        return squares

    def move(self, direction: Vector, num_squares: int, pushed: Optional[Entity] = None) -> None:
        """
        Attempts to move the Mech in a certain direction a certain number of squares.
        Moving onto a Minion stomps the Minion. Pushing and towing logic is contained as well.
        Works by pushing movement commands onto the prompt stack
        :param direction: Vector representing the direction in which the movement should occur
        :param num_squares: number of movement steps
        :param pushed: If the movement was due to pushing, input the Entity which did the pushing, otherwise, input nothing
        :return: None
        """

        remaining_moves: int = num_squares
        # If the Mech was pushed, just move, ignoring any towing checks
        if pushed:
            while remaining_moves > 0:
                successfully_moved: bool = self.movement_logic(direction)
                if not successfully_moved:
                    break
                remaining_moves -= 1
            return

        def move_1(mech_1: Mech, choice_1: int, remaining_moves_1: int) -> None:
            """Scans for towable objects"""
            if remaining_moves_1 == 0:
                return
            if not mech_1.can_move(mech_1.position, direction):
                return
            towable_objects_positions: List[Vector] = []
            if remaining_moves_1 >= 2:
                towable_objects_positions = mech_1.scan(1, 'Mechs', direction)
            num_choices_1: int = len(towable_objects_positions) + 1

            def move_2(mech_2: Mech, choice_2: int, remaining_moves_2: int) -> None:
                """Move and then tow the desired object (or not)"""
                # only tow if the movement is actually successful
                mech_2.movement_logic(direction)
                towing_destination: Vector = mech_2.position - direction
                # the first choice implies no towing
                if choice_2 == 0:
                    no_towing: Callable[[Mech, int], None] = partial(move_1, remaining_moves_1=remaining_moves_2-1)
                    pure_move_completed: Prompt = Prompt(1, no_towing)
                    mech_2.stack_push(pure_move_completed)
                elif choice_2 != 0:
                    towed_object_location: Vector = towable_objects_positions[choice_2 - 1]
                    towed_object: Entity = mech_2.board[vector_to_tuple(towed_object_location)].thing
                    towed_object.raw_move(towed_object_location, towing_destination)
                    towing: Callable[[Mech, int], None] = partial(move_1, remaining_moves_1=remaining_moves_2-2)
                    towing_move_completed: Prompt = Prompt(1, towing)
                    mech_2.stack_push(towing_move_completed)

            tow_plus_move: Callable[[Mech, int], None] = partial(move_2, remaining_moves_2=remaining_moves_1)
            towing_prompt: Prompt = Prompt(num_choices_1, tow_plus_move)
            mech_1.stack_push(towing_prompt)

        begin_movement_chain: Callable[[Mech, int], None] = partial(move_1, remaining_moves_1=remaining_moves)
        begin_movement_chain_prompt: Prompt = Prompt(1, begin_movement_chain)
        self.stack_push(begin_movement_chain_prompt)

    def take_damage(self) -> None:
        """
        Draws a damage card -- this will be implemented much later
        :return: None
        """
        raise NotImplementedError

    def scythe(self, level: int) -> None:

        def scythe_1(mech_1: Mech, choice_1: int) -> None:
            """Scans around the mech for targetable minions"""
            squares_with_minions: List[Vector] = mech_1.scan(1, 'Minions')
            # if there are fewer minions than the card lets you hit, then there is 1 possible way to deal damage
            if len(squares_with_minions) < level:
                damage_combinations: List[tuple[Vector]] = [tuple(squares_with_minions)]
            else:
                damage_combinations: List[tuple[Vector]] = list(combinations(squares_with_minions, level))
            num_damage_combinations: int = len(damage_combinations)

            def scythe_2(mech_2: Mech, choice_2: int) -> None:
                """Damages a specific set of squares (with Minions) and rotates by a specific angle"""
                chosen_strike, turn_angle = divmod(num_damage_combinations, choice_2)
                targeted_squares: List[Vector] = list(damage_combinations[chosen_strike])
                mech_2.damage_multiple(targeted_squares)
                match choice_2:
                    case 0:
                        mech_2.turn(90)
                    case 1:
                        mech_2.turn(-90)
                    case 2:
                        mech_2.turn(180)
                    case 3:
                        mech_2.turn(0)

            scythe_damage_and_turn = Prompt(num_damage_combinations * (level + 1), scythe_2)
            mech_1.stack_push(scythe_damage_and_turn)

        scythe_scan = Prompt(1, scythe_1)
        self.stack_push(scythe_scan)

    def skewer(self, level: int) -> None:

        def skewer_1(mech_1: Mech, choice_1: int) -> None:
            mech_1.move(mech_1.orientation, level)

        skewer_command = Prompt(1, skewer_1)
        self.stack_push(skewer_command)

    def ripsaw(self, level: int) -> None:

        def ripsaw_1(mech_1: Mech, choice_1: int) -> None:
            # scan for the targets
            target_squares: List[Vector] = []
            pointer: Vector = mech_1.position + mech_1.orientation
            ripsaws_left = level
            while oob_check(mech_1.board, pointer) and ripsaws_left > 0:
                curr_square: Tile = mech_1.board[vector_to_tuple(pointer)]
                if curr_square.has_friendly() or curr_square.has_wall():
                    break
                elif curr_square.has_minion():
                    target_squares.append(pointer.copy())
                    ripsaws_left -= 1
                pointer += mech_1.orientation
            # hit them
            mech_1.damage_multiple(target_squares)

        ripsaw_command = Prompt(1, ripsaw_1)
        self.stack_push(ripsaw_command)

    def fuel_tank(self, level: int) -> None:

        def fuel_tank_1(mech_1: Mech, choice_1: int) -> None:
            match choice_1:
                case 0:
                    mech_1.turn(90)
                case 1:
                    mech_1.turn(-90)
                case 2:
                    mech_1.turn(180)
                case 3:
                    mech_1.turn(0)

        fuel_tank_command = Prompt(level + 1, fuel_tank_1)
        self.stack_push(fuel_tank_command)

    def blaze(self, level: int) -> None:

        def blaze_1(mech_1: Mech, choice_1: int) -> None:

            def blaze_2_damage(mech_2: Mech, choice_2: int) -> None:
                """Executes the damage of Blaze (hits the squares to the left and right after the movement)"""
                left_and_right: List[Vector] = [
                    mech_2.position + rotate(mech_2.orientation, 90),
                    mech_2.position + rotate(mech_2.orientation, -90)
                ]
                mech_2.damage_multiple(left_and_right)

            blaze_damage_component = Prompt(1, blaze_2_damage)

            # places the damage below the movement
            mech_1.stack_push(blaze_damage_component)
            mech_1.move(mech_1.orientation, level)

        blaze_command = Prompt(1, blaze_1)
        self.stack_push(blaze_command)

    def flamespitter(self, level: int) -> None:

        def flamespitter_1(mech_1: Mech, choice_1: int) -> None:
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

            mech_1.damage_multiple(target_squares)

        flamespitter_command = Prompt(1, flamespitter_1)
        self.stack_push(flamespitter_command)

    def cyclotron(self, level: int) -> None:

        def cyclotron_1(mech_1, choice_1: int) -> None:
            target_squares: List[Vector] = []
            for i in range(1, level + 1):
                target_squares += [mech_1.position + np.array(coordinate_pair) for coordinate_pair in
                                   product((-i, i), (-i, i))]
            mech_1.damage_multiple(target_squares)
            match choice_1:
                case 0:
                    mech_1.turn(90)
                case 1:
                    mech_1.turn(-90)
                case 2:
                    mech_1.turn(180)
                case 3:
                    mech_1.turn(0)

        cyclotron_command = Prompt(level + 1, cyclotron_1)
        self.stack_push(cyclotron_command)

    def speed(self, level: int) -> None:

        def speed_1(mech_1: Mech, choice_1: int) -> None:
            match choice_1:
                case 0:
                    mech_1.move(mech_1.orientation, level)
                case 1:
                    mech_1.move(mech_1.orientation, level + 1)
                case 2:
                    mech_1.move(mech_1.orientation, level + 2)
                case 3:
                    mech_1.move(mech_1.orientation, level + 3)

        speed_command = Prompt(level + 1, speed_1)
        self.stack_push(speed_command)

    def chain_lightning(self, level: int) -> None:

        def chain_check(mech: Mech, curr_square: Vector, alr_hit_squares: List[Vector]) -> List[Vector]:
            """Helper function"""
            available_chaining_squares: List[Vector] = []
            diagonals: List[Vector] = [curr_square + np.array(coordinate_pair) for coordinate_pair in
                                       product((-1, 1), (1, 1))]
            for square in diagonals:
                if oob_check(square):
                    if mech.board[vector_to_tuple(square)].has_minion():
                        if not any(np.array_equal(square, arr) for arr in alr_hit_squares):
                            available_chaining_squares.append(square)
            return available_chaining_squares

        def chain_lightning_1(mech_1: Mech, choice_1: int) -> None:
            """Scans the 3 squares in front of the Mech for a first target"""
            squares_in_front: List[Vector] = [
                mech_1.position + mech_1.orientation,
                mech_1.position + mech_1.orientation + rotate(mech_1.orientation, -90),
                mech_1.position + mech_1.orientation + rotate(mech_1.orientation, 90)
            ]

            def chain_lightning_2(mech_2: Mech, choice_2: int, prev_hit_squares: List[Vector],
                                  avail_squares: List[Vector]) -> None:
                """Handles chaining"""
                # early exit if max depth is reached
                if len(prev_hit_squares) >= level * 2:
                    mech_2.damage_multiple(prev_hit_squares)
                    return
                curr_square: Vector = avail_squares[choice_2]
                prev_hit_squares_new = prev_hit_squares.copy() + [curr_square]
                chaining_targets: List[Vector] = chain_check(mech_2, curr_square, prev_hit_squares_new)
                # early exit if a target to chain to was not found
                if len(chaining_targets) == 0:
                    mech_2.damage_multiple(prev_hit_squares_new)
                    return
                # otherwise, add the next chain to the function stack
                num_available_chains: int = len(chaining_targets)
                next_chain: Callable[[Mech, int], None] = partial(chain_lightning_2,
                                                                  prev_hit_squares=prev_hit_squares_new,
                                                                  avail_squares=chaining_targets)
                next_chain_prompt = Prompt(num_available_chains, next_chain)
                mech_2.stack_push(next_chain_prompt)

            first_square = squares_in_front[choice_1]
            if oob_check(mech_1.board, first_square):
                if mech_1.board[vector_to_tuple(first_square)].has_minion():
                    first_chain_targets: List[Vector] = chain_check(mech_1, first_square, [])
                    # early exit if unable to chain
                    if len(first_chain_targets) == 0:
                        mech_1.damage(first_square)
                        return
                    # otherwise, begin the chain process
                    num_first_available_chains: int = len(first_chain_targets)
                    first_chain: Callable[[Mech, int], None] = partial(chain_lightning_2, prev_hit_squares=first_square,
                                                                       avail_squares=first_chain_targets)
                    first_chain_prompt = Prompt(num_first_available_chains, first_chain)
                    mech_1.stack_push(first_chain_prompt)

        chain_lightning_command = Prompt(3, chain_lightning_1)
        self.stack_push(chain_lightning_command)

    def memory_core(self, level: int) -> None:

        def memory_core_1(mech_1, choice_1: int) -> None:
            match choice_1:
                case 0:
                    mech_1.turn(90)
                case 1:
                    mech_1.turn(-90)
                case 2:
                    mech_1.turn(180)
                case 3:
                    mech_1.turn(0)

        memory_core_command = Prompt(level + 1, memory_core_1)
        self.stack_push(memory_core_command)

    def omnistomp(self, level: int) -> None:

        def omnistomp_1(mech_1: Mech, choice_1: int) -> None:
            match choice_1:
                case 0:
                    mech_1.move(rotate(mech_1.orientation, 90), level)
                case 1:
                    mech_1.move(mech_1.orientation, level)
                case 2:
                    mech_1.move(rotate(mech_1.orientation, -90), level)

        omnistomp_command = Prompt(3, omnistomp_1)
        self.stack_push(omnistomp_command)

    def hexmatic_aimbot(self, level: int) -> None:

        def hexmatic_aimbot_1(mech_1: Mech, choice_1: int) -> None:
            """Scans for targets"""
            target_squares: List[Vector] = mech_1.scan(3, 'Minions')
            num_choices: int = len(target_squares)

            def hexmatic_aimbot_2(mech_2: Mech, choice_2: int) -> None:
                mech_2.damage(target_squares[choice_2])

            hexmatic_aimbot_damage = Prompt(num_choices, hexmatic_aimbot_2)
            mech_1.stack_push(hexmatic_aimbot_damage)

        hexmatic_aimbot_scan = Prompt(1, hexmatic_aimbot_1)
        self.stack_push(hexmatic_aimbot_scan)

    translations: Dict[str, Callable[[Mech, int], Prompt | None]] = {
        'Scythe': scythe, 'Skewer': skewer, 'Ripsaw': ripsaw,
        'Fuel Tank': fuel_tank, 'Blaze': blaze, 'Flamespitter': flamespitter,
        'Cyclotron': cyclotron, 'Speed': speed, 'Chain Lightning': chain_lightning,
        'Memory Core': memory_core, 'Omnistomp': omnistomp, 'Hexmatic Aimbot': hexmatic_aimbot,
        'Empty': lambda x, y: None
    }

    def read_command_line(self) -> None:
        """
        Translates all the information on the command line into prompt objects and pushes them to the prompt stack
        :return: None
        """
        for slot in range(1, 7)[::-1]:
            command_card_string = self.command_line[slot - 1][0]
            command_card_level = self.command_line[slot - 1][1]
            command_card_method: Callable[[Mech, int], None] = self.translations[command_card_string]
            command_card_method(self, command_card_level)
