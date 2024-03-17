from ..object_templates.template_location import *

windergard = Location()

# Notes on create area interactions not longer than 5

windergard.create_area("Caravan", {"1":"Town Square", "2":"Cancel"}, [None], ["test", "test2", "", "", ""], [None])
windergard.create_area("Town Square", {"1":"Blacksmith", "2":"Training ground", "3":"General store", "4":"Inn", "5":"Cancel"}, [None], ["test", "test2", "", "", ""], [None])

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
