from ..locations.windengard.windengard_location import *

# Contains all locations data
class LocationDatabase:

    def __init__(self, item_database, player_reference):
        
        # --------------------- Locations database --------------------- #

        self.windengard_reference = Windergard(item_database, player_reference)

        self.locations_database = {"windengard":self.windengard_reference.all_areas}
