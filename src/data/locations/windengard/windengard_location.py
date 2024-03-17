from ..object_templates.template_location import *

windergard = Location()

# Notes on create area interactions not longer than 5

class test:

    def run_logic():
        print("test")

class test2:

    def run_logic():
        print("test2")


windergard.create_area(area_name="Caravan", 
                       move_areas={"1":"Town Square", "2":"Cancel"}, 
                       quests={None:None}, 
                       interactions={"test":test, "test2":test2}, 
                       npcs={None:None})

windergard.create_area(area_name="Town Square", 
                       move_areas={"1":"Blacksmith", "2":"Training ground", "3":"General store", "4":"Inn", "5":"Cancel"}, 
                       quests={None:None}, 
                       interactions={"test":"", "test2":""}, 
                       npcs={None:None})

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
