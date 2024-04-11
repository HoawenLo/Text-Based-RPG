from ..object_templates.template_location import *
from .windengard_npcs import WindergardNPCs
from .windengard_interactions import WindengardInteractions
from .windengard_quests import WindengardQuests


class Windergard:

    def __init__(self, item_database, player_reference):

        # --------------------- Location logic --------------------- #

        location = Location()

        windergard_npcs = WindergardNPCs(item_database, player_reference)

        self.npcs = {
            "blacksmith":windergard_npcs.npc_packages(npc_reference="blacksmith"),
            "oldman":windergard_npcs.npc_packages(npc_reference="oldman"),
            "oldman_intro":windergard_npcs.npc_packages(npc_reference="oldman_intro"),
            "rookie_trainer":windergard_npcs.npc_packages(npc_reference="rookietrainer"),
            "villager_ts":windergard_npcs.npc_packages(npc_reference="villager_ts"),
            "general_store":windergard_npcs.npc_packages(npc_reference="general_store"),
            "villagers_inn":windergard_npcs.npc_packages(npc_reference="villagers_inn")
        }

        windengard_interactions = WindengardInteractions(player_reference, npc_database=self.npcs, npc_conds=None)
        
        quest_rewards = {"tutorial_quest":{"exp":20, "gold":50, "Apple": (item_database["Apple"], 2)}}
        
        self.windengard_quests = WindengardQuests(rewards=quest_rewards, 
                                                  item_database=item_database, 
                                                  npc_database=self.npcs, 
                                                  player_reference=player_reference)

        # Notes on create area interactions not longer than 5

        location.create_area(area_name="Caravan", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={}, 
                            npcs={})

        location.create_area(area_name="Town Square", 
                            move_areas={"1":"Blacksmith", "2":"Training ground", "3":"General store", "4":"Inn", "5":"Cancel"}, 
                            quests={}, 
                            interactions={"Talk to old man":windengard_interactions.all_interactions["oldman_dialogue"], 
                                          "Talk to villager":windengard_interactions.all_interactions["villager_ts_dialogue"],
                                          "Pet stray dog":windengard_interactions.all_interactions["pet_dog"]}, 
                            npcs={"Old man":self.npcs["oldman"], "Villager":self.npcs["villager_ts"]})
        
        location.create_area(area_name="Blacksmith", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={"Talk to blacksmith":windengard_interactions.all_interactions["blacksmith_dialogue"]}, 
                            npcs={"Blacksmith":self.npcs["blacksmith"]})
        
        location.create_area(area_name="Training ground", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={"Combat":windengard_interactions.all_interactions["combat"]}, 
                            npcs={})
        
        location.create_area(area_name="General store", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={"Talk to general store trader": windengard_interactions.all_interactions["general_store_dialogue"]}, 
                            npcs={"General store trader":self.npcs["general_store"]})
        
        location.create_area(area_name="Inn", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={"Eavesdrop on conversation":windengard_interactions.all_interactions["villagers_inn_dialogue"]}, 
                            npcs={"Villagers inn":self.npcs["villagers_inn"]})

        self.all_areas = location.all_areas

if __name__ == "__main__":
    import sys

    # filepath = r"C:\Users\Hoawen\Desktop\Programming\Python\Text based rpg\Alpha Version 2\data\locations\object_templates"
    # sys.path.append(filepath)

    # from template_location import Location

    # windergard = Location()

    # windergard.create_area("Caravan", ["Town Square"], [None], [None], [None])

    # all_areas = windergard.all_areas

    # print(all_areas)

    # print(dir(windergard))
