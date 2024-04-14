from .items.item_data import ItemDatabase
from .locations.all_locations import LocationDatabase
from .player_mechanics.player_mechanics import Player

class GameData:

    def __init__(self, player_reference):
        
        # This is messy but couldn't be bothered to reorganise everything to find a way to access the intro quest.
        self.location_data = LocationDatabase(ItemDatabase(player_reference).item_database, player_reference)
        location_database = self.location_data.locations_database

        self.game_data = {"items":ItemDatabase(player_reference).item_database, 
                          "locations":location_database, 
                          "player":Player,
                          "intro_quest":self.location_data}

 
