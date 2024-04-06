from ..object_templates.interactions_templates import *

class WindengardInteractions:

    def __init__(self, player_reference, npc_database):

        blacksmith_dialogue = Interactions(logic_input=npc_database["blacksmith"].run_trading_dialogue,
                                           player_reference=player_reference)

        self.all_interactions = {"blacksmith_dialogue":blacksmith_dialogue}
