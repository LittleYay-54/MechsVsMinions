from board import Board
from entities import Mech
from typing import List
from auxiliary_functions import Prompt
from copy import deepcopy


# The engine logic shall be contained here.
# Here is the plan:
# the code should be built in a way such that the game could be playable through a GUI.
# The engine should *merely make choices on behalf of a would-be player*.
# Therefore, executing command cards should not cause branches themselves,
# instead they should raise some sort of user-input prompt
# which the engine can then "automate", and create branches as necessary

def win_check(board: Board) -> bool:
    """
    Checks if the puzzle is solved
    :param board: the game board
    :return: True if completed, False if failed
    """
    if board.count_minions() == 0:
        # here check if the bomb is on the repair pad
        print("A winning line was found")
        return True
    else:
        return False

def engine(board: Board, mech: Mech) -> None:
    """Good Luck"""
    # DFS
    mech.read_command_line()
    mech_stack: List[Mech] = [mech]
    while mech_stack:
        curr_mech: Mech = mech_stack.pop()
        top_prompt: Prompt = curr_mech.prompt_stack.pop()

        for i in range(1, top_prompt.num_options)[::-1]:
            copy_mech: Mech = deepcopy(curr_mech)
            top_prompt.executable(copy_mech, i)
            if not copy_mech.prompt_stack:
                win_check(copy_mech.board)
            else:
                mech_stack.append(copy_mech)

        top_prompt.executable(curr_mech, 0)
        if not curr_mech.prompt_stack:
            win_check(curr_mech.board)
        else:
            mech_stack.append(curr_mech)
