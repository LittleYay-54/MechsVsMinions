from abc import ABC, abstractmethod
from board import Board
from types import Vector
from functions import tuple_to_vector, vector_to_tuple, oob_check, rotate



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
