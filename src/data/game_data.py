from .items.item_data import ItemDatabase
from .locations.all_locations import LocationDatabase
from .player_mechanics.player_mechanics import Player

class GameData:

    def __init__(self, player_reference):

        location_database = LocationDatabase(ItemDatabase(player_reference).item_database, player_reference).locations_database

        self.game_data = {"items":ItemDatabase, 
                          "locations":location_database, 
                          "player":Player}

 
