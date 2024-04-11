import time

from ..object_templates.interactions_templates import *

class WindengardInteractions:

    def __init__(self, player_reference, npc_database, npc_conds):

        
        
        # ------------- Misc logic inputs ------------- #

        def pet_dog_logic(placeholder):
            """Pet a dog."""
            pet_interaction = "You pet the dog."
            pet_response = "Dog: Woof! Woof!"
            self.word_crawl(pet_interaction)
            self.word_crawl(pet_response)
            

        # ------------- Misc ------------- #

        pet_dog = Interactions(logic_input=pet_dog_logic, 
                               player_reference=player_reference)

        # ------------- Combat ------------- #

        # self.npc_conds = npc_conds

        combat = Combat(player_reference=player_reference, local_npc_database=npc_database, npc_conds=None)

        # ------------- Dialogue ------------- #

        blacksmith_dialogue = Interactions(logic_input=npc_database["blacksmith"].run_trading_dialogue,
                                           player_reference=player_reference)
        general_store_dialogue = Interactions(logic_input=npc_database["general_store"].run_trading_dialogue,
                                           player_reference=player_reference)
        oldman_dialogue = Interactions(logic_input=npc_database["oldman"].run_dialogue,
                                           player_reference=player_reference)

        villager_ts_dialogue = Interactions(logic_input=npc_database["villager_ts"].run_dialogue, 
                                            player_reference=player_reference)
        
        villagers_inn_dialogue = Interactions(logic_input=npc_database["villagers_inn"].run_dialogue, 
                                            player_reference=player_reference)

        self.all_interactions = {"blacksmith_dialogue":blacksmith_dialogue,
                                 "oldman_dialogue":oldman_dialogue,
                                 "villager_ts_dialogue":villager_ts_dialogue,
                                 "general_store_dialogue":general_store_dialogue,
                                 "villagers_inn_dialogue":villagers_inn_dialogue,
                                 "pet_dog":pet_dog,
                                 "combat":combat}

        # ------------- Text manipulation ------------- #

    def word_crawl(self, text, line_length=60, text_speed=0.1):
        """Used to crawl text. Crawls words instead of 
        single characters.
        
        Args:
            text: The sentence to be crawled.
            line_length: Sets the length of the line.
            If has a large body of text, will move 
            onto next line if line length reached."""

        words = text.split()
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= line_length:
                current_line += word + " "
            else:
                print(current_line)
                current_line = word + " "
                time.sleep(text_speed)

            print(current_line, end="\r")
            time.sleep(text_speed)

        print(current_line)