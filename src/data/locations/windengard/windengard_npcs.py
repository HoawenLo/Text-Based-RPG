from ..object_templates.npc_templates import *

def trader_dialogue_package(*args):
    """Dialogue package for trader.
    
    Params:
        *args: Accepts any number of arguments as 
        run_dialogue method for NPC varies.
    """

    trader_dialogue = Dialogue()

    if len(*args) == 3:
        trader_dialogue.set_special_functions(*args[1])
    if len(*args) == 5:
        trader_dialogue.set_special_functions(*args[1], *args[2])

    # Dialogue below
