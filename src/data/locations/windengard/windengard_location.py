from ..object_templates.template_location import *
from .windengard_npcs import WindergardNPCs

windergard = Location()

npcs = {
    "blacksmith":WindergardNPCs.npc_packages(npc_reference="blacksmith"),
}

# Notes on create area interactions not longer than 5

windergard.create_area(area_name="Caravan", 
                       move_areas={"1":"Town Square", "2":"Cancel"}, 
                       quests={}, 
                       interactions={}, 
                       npcs={})

windergard.create_area(area_name="Town Square", 
                       move_areas={"1":"Blacksmith", "2":"Training ground", "3":"General store", "4":"Inn", "5":"Cancel"}, 
                       quests={}, 
                       interactions={"test":"", "test2":""}, 
                       npcs={"Blacksmith":npcs["blacksmith"]})

all_areas = windergard.all_areas

if __name__ == "__main__":
    import sys

    filepath = r"C:\Users\Hoawen\Desktop\Programming\Python\Text based rpg\Alpha Version 2\data\locations\object_templates"
    sys.path.append(filepath)

    from template_location import Location

    windergard = Location()

    windergard.create_area("Caravan", ["Town Square"], [None], [None], [None])

    all_areas = windergard.all_areas

    print(all_areas)

    # print(dir(windergard))
