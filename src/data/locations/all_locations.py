from ..locations.windengard.windengard_location import *

# Contains all locations data
class LocationDatabase:

    def __init__(self, item_database, player_reference):
        
        # --------------------- Locations database --------------------- #

        self.locations_database = {"windengard":Windergard(item_database, player_reference).all_areas}