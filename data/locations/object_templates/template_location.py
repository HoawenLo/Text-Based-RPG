# template location

class Location():

    def __init__(self):
        pass

    def create_area(self, area_name, move_areas, quests, interactions, npcs):
        
        area_data = {"areas":move_areas,
                     "quests":quests, 
                     "interactions":interactions, 
                     "npcs":npcs}
        
        setattr(self, area_name, area_data)