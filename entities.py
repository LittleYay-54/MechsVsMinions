from abc import ABC, abstractmethod
from board import Board
from types_1 import Vector
from copy import deepcopy
from itertools import product
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
        self.board.minion_count -= 0 


class Mech(Entity):
    def __init__(self, board: Board, position: Vector, orientation: Vector, command_line: list) -> None:
        super().__init__(board, position, orientation)
        self.board = deepcopy(board)
        self.curr_slot = 1
        self.command_line = command_line
        self.execute()


    def take_damage(self) -> None:
        # this will be implemented much later
        pass

    def blaze(self, level: int) -> None:
        for i in range(level):
            self.move(self.orientation)
        self.damage(self.position + rotate(self.orientation, -90))
        self.damage(self.position + rotate(self.orientation, 90))

    def fuel_tank(self, level: int, rotation) -> None:
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

    def speed(self, level: int, distance: int) -> None:
        pass

    def cyclotron(self, level: int) -> None:
        for i in range(1, level+1):
            self.damage(self.position + [[i], [i]])
            self.damage(self.position + [[-i], [i]])
            self.damage(self.position + [[i], [-i]])
            self.damage(self.position + [[-i], [-i]])
            
    def chain_lightning(self, level: int, target: int) -> None:
        pass
    def cl_chain(self, position: Vector, target: int) -> bool:
        pass
    

    

    def skewer(self, level: int) -> None:
        for i in range(level):
            self.move(self.orientation)
        #shield functonality eventually

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
    cardtype = {"sk": skewer,
            "r": ripsaw,
            "sc": scythe,
            "ft": fuel_tank,
            'a': hexmatic_aimbot,
            'm': memory_core,
            'cl':chain_lightning,
            "b": blaze,
            "c": cyclotron,
            "f": flamespitter,
            "o": omnistomp,
            "sp": speed,
            }
    def execute(self):
        if self.curr_slot == 7 and self.board.minion_count == 0:
            print(f"This is a winning command line: {self.text}")
            return
        command = self.command_line[self.curr_slot - 1]
        try:
            level = int(command[-1])
            card = command.replace(str(level), '')
        except ValueError:
            level = 1
            card = command
        self.cardtype[card](level)
        self.curr_slot += 1
        if card in ["o",  "c",  "sp"]:
            return
        # if self.curr_slot < 7:
            # print(f"Call number: BLANK, number of minions remaining: {len(self.temp_minions)}, locations of the minions: {self.temp_minions}, Commands executed so far: {self.text}")
        self.execute()
class TristanaEngine(Mech):
    def __init__(self, board: Board, position: Vector, orientation: Vector, command_line: list, curr_slot: int = 1) -> None:
        super().__init__(board, position, orientation, command_line)
        self.curr_slot = curr_slot
        self.execute()
    def turn(self, level):
        pass
    def blaze(self, level: int) -> None:
        super().blaze(level)

    def fuel_tank(self, level: int) -> None:
        pass

    def flamespitter(self, level: int) -> None:
        super().flamespitter(level)
    def speed(self, level: int) -> None:
        for option in [1,2]:
            position = self.position + self.orientation*((level-1)*2+option)
            TristanaEngine(self.board, position, self.orientation, self.command_line, self.curr_slot+1)

    def cyclotron(self, level: int) -> None:
        super().cyclotron(level)

        # turn functionality

    def chain_lightning(self, level: int) -> None:
        for target in [1,2,3]:
            location = rotate(self.orientation, (target - 2)*90) + self.position
            if type(self.board[location].thing) == Minion:
                branch = TristanaEngine(self.board, self.position, self.orientation, self.command_line[self.curr_slot:], self.curr_slot)
                branch.damage(location)
                max_depth = 1+(level-1)*2
                branch.cl_chain(location, self.command_line, 0, max_depth)

        
    def cl_chain(self, position: Vector, command_line, current_depth, max_depth) -> None:
        if current_depth < max_depth:
            return
        for target in position + product((-1,1),(-1,1)):
            if type(self.board[target].thing) == Minion:
                branch = TristanaEngine(self.board, self.position, self.orientation, self.command_line[self.curr_slot:], self.curr_slot)
                branch.damage(target)
                branch.cl_chain(target, command_line, current_depth+1, max_depth)
            else:
                TristanaEngine(self.board, self.position, self.orientation, command_line[:self.curr_slot], self.curr_slot+ 1)


    def skewer(self, level: int) -> None:
        super().skewer(level)

    def scythe(self, level: int) -> None:
        pass

    def ripsaw(self, level: int) -> None:
        pass

    def omnistomp(self, level: int) -> None:
        pass

    def memory_core(self, level: int) -> None:
        pass

    def hexmatic_aimbot(self, level: int) -> None:
        for x,y in product(range(self.position[0][0]-level, self.position[0][0]+level), range(self.position[1][1]-level, self.position[1][1]+level)):
            if type(self.board[[x],[y]].thing) == Minion:
                branch = TristanaEngine(self.board, self.position, self.orientation, self.command_line[:self.curr_slot], self.curr_slot)
                branch.damage([[x],[y]])
                TristanaEngine(branch.board, branch.position, branch.orientation, branch.command_line[self.curr_slot:], self.curr_slot+1)
 
    cardtype = {"sk": skewer,
            "r": ripsaw,
            "sc": scythe,
            "ft": fuel_tank,
            'a': hexmatic_aimbot,
            'm': memory_core,
            'cl':chain_lightning,
            "b": blaze,
            "c": cyclotron,
            "f": flamespitter,
            "o": omnistomp,
            "sp": speed,
            }
    def execute(self):
        if self.curr_slot == 7 and self.board.minion_count == 0:
            print(f"This is a winning command line: {self.text}")
            return
        command = self.command_line[self.curr_slot - 1]
        try:
            level = int(command[-1])
            card = command.replace(str(level), '')
        except ValueError:
            level = 1
            card = command
        self.cardtype[card](level)
        self.curr_slot += 1
        if card in ["o",  "c",  "sp"]:
            return
        # if self.curr_slot < 7:
            # print(f"Call number: BLANK, number of minions remaining: {len(self.temp_minions)}, locations of the minions: {self.temp_minions}, Commands executed so far: {self.text}")
        self.execute()
        
class PlayerMech(Mech):
    def __init__(self, board: Board, position: Vector, orientation: Vector, command_line: list) -> None:
        super().__init__(board, position, orientation, command_line)
        self.curr_slot = 1
        self.execute()
    def turn(self, level):
        pass

    def take_damage(self) -> None:
        # this will be implemented much later
        pass

    def blaze(self, level: int) -> None:
        super().blaze(level)

    def fuel_tank(self, level: int, rotation) -> None:
        pass

    def flamespitter(self, level: int) -> None:
        super().flamespitter(level)

    def speed(self, level: int, distance: int) -> None:
        pass

    def cyclotron(self, level: int) -> None:
        super().cyclotron(level)

        # turn functionality

    def chain_lightning(self, level: int, target: int) -> None:
        pass
    def cl_chain(self, position: Vector, target: int) -> bool:
        pass
    

    

    def skewer(self, level: int) -> None:
        super().skewer(level)
        #shield functonality eventually

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
    cardtype = {"sk": skewer,
            "r": ripsaw,
            "sc": scythe,
            "ft": fuel_tank,
            'a': hexmatic_aimbot,
            'm': memory_core,
            'cl':chain_lightning,
            "b": blaze,
            "c": cyclotron,
            "f": flamespitter,
            "o": omnistomp,
            "sp": speed,
            }
    def execute(self):
        if self.curr_slot == 7 and self.board.minion_count == 0:
            print(f"This is a winning command line: {self.text}")
            return
        command = self.command_line[self.curr_slot - 1]
        try:
            level = int(command[-1])
            card = command.replace(str(level), '')
        except ValueError:
            level = 1
            card = command
        self.cardtype[card](level)
        self.curr_slot += 1
        if card in ["o",  "c",  "sp"]:
            return
        # if self.curr_slot < 7:
            # print(f"Call number: BLANK, number of minions remaining: {len(self.temp_minions)}, locations of the minions: {self.temp_minions}, Commands executed so far: {self.text}")
        self.execute()