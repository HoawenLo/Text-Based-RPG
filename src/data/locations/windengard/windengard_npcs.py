from ..object_templates.npc_templates import *

class WindergardNpcs:

    def __init__(self):

        

        self.npc_database = {}

    def dialogue_packages(self):
        """Holds the dialogue packages.
        
        """


def trader_dialogue_package(*args):
    """Dialogue package for trader.
    
    Args:
        *args: Accepts any number of arguments as 
        run_dialogue method for NPC varies.

    Returns:
        None
    """

    trader_dialogue = Dialogue()

    if len(*args) == 3:
        trader_dialogue.set_special_functions(*args[1])
    if len(*args) == 5:
        trader_dialogue.set_special_functions(*args[1], *args[2])

    # Dialogue below
        
    a = ("Trader: Hello", trader_dialogue.dialogue_npc)
    b = ("Hello", trader_dialogue.dialogue_player)
    c = ("NPC: How can I help?", trader_dialogue.dialogue_npc)
    d = ((("end", trader_dialogue.end_dialogue), ("show items", trader_dialogue.run_special_function), trader_dialogue.show_responses))
    e = ("end", trader_dialogue.end_dialogue)
    f = ("show items", trader_dialogue.run_special_function)
    g = ("chat", trader_dialogue.dialogue_npc)

    trader_dialogue.initialise_node(a)
    trader_dialogue.add_dialogue_node(b)
    trader_dialogue.add_dialogue_node(c)
    trader_dialogue.add_dialogue_node(d)
    trader_dialogue.add_dialogue_node(e)
    trader_dialogue.add_dialogue_node(f)
    trader_dialogue.add_dialogue_node(g)

    trader_dialogue.add_dialogue_edge(a, b)
    trader_dialogue.add_dialogue_edge(b, c)
    trader_dialogue.add_dialogue_edge(c, d)
    trader_dialogue.add_dialogue_edge(d, e)
    trader_dialogue.add_dialogue_edge(d, f)
    trader_dialogue.add_dialogue_edge(d, g)
    trader_dialogue.add_dialogue_edge(f, e)
    trader_dialogue.add_dialogue_edge(g, e)

    trader_dialogue.run_dialogue()

trader_dialogue_package()
        
    
