from board import Board
from entities import Mech
from typing import List, Dict, Callable
from functools import partial

# The engine logic shall be contained here.
# Here is the plan:
# the code should be built in a way such that the game could be playable through a GUI.
# The engine should *merely make choices on behalf of a would-be player*.
# Therefore, executing command cards should not cause branches themselves,
# instead they should raise some sort of user-input prompt
# which the engine can then "automate", and create branches as necessary

def engine(board: Board, mech: Mech):
    def translate(mech: Mech) -> Callable[[], Prompt]:
        card_to_method: Dict[str, Callable[[], None]] = {
            'Scythe': mech.scythe, 'Skewer': mech.skewer, 'Ripsaw': mech.ripsaw,
            'Fuel Tank': mech.fuel_tank, 'Blaze': mech.blaze, 'Flamespitter': mech.flamespitter,
            'Cyclotron': mech.cyclotron, 'Speed': mech.speed, 'Chain Lightning': mech.chain_lightning,
            'Memory Core': mech.memory_core, 'Omnistomp': mech.omnistomp, 'Hexmatic Aimbot': mech.hexmatic_aimbot,
            'Empty': lambda x: None
        }
        sequence: List[Callable[[], None]] = []
        for card, level in mech.command_line:
            sequence.append(partial(card_to_method[card], level))
        return sequence

    def search(mechstate)
