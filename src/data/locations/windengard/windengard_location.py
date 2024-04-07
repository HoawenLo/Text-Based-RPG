from ..object_templates.template_location import *
from .windengard_npcs import WindergardNPCs
from .windengard_interactions import WindengardInteractions


class Windergard:

    def __init__(self, item_database, player_reference):

        # --------------------- Location logic --------------------- #

        location = Location()

        windergard_npcs = WindergardNPCs(item_database, player_reference)

        npcs = {
            "blacksmith":windergard_npcs.npc_packages(npc_reference="blacksmith"),
        }

        windengard_interactions = WindengardInteractions(player_reference, npc_database=npcs)

        # Notes on create area interactions not longer than 5

        location.create_area(area_name="Caravan", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={}, 
                            npcs={})

        location.create_area(area_name="Town Square", 
                            move_areas={"1":"Blacksmith", "2":"Training ground", "3":"General store", "4":"Inn", "5":"Cancel"}, 
                            quests={}, 
                            interactions={}, 
                            npcs={})
        
        location.create_area(area_name="Blacksmith", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={"Talk to blacksmith":windengard_interactions.all_interactions["blacksmith_dialogue"]}, 
                            npcs={"Blacksmith":npcs["blacksmith"]})
        
        location.create_area(area_name="Training ground", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={}, 
                            npcs={})
        
        location.create_area(area_name="General store", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={}, 
                            npcs={})
        
        location.create_area(area_name="Inn", 
                            move_areas={"1":"Town Square", "2":"Cancel"}, 
                            quests={}, 
                            interactions={}, 
                            npcs={})

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
