from board import Board
from entities import Mech
from typing import List, Dict, Callable
from functools import partial
from auxiliary_functions import Prompt

# The engine logic shall be contained here.
# Here is the plan:
# the code should be built in a way such that the game could be playable through a GUI.
# The engine should *merely make choices on behalf of a would-be player*.
# Therefore, executing command cards should not cause branches themselves,
# instead they should raise some sort of user-input prompt
# which the engine can then "automate", and create branches as necessary


def engine(board: Board, mech: Mech):
    pass

