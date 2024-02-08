from npc import mottengard_npcs
import item

# Map database

class Map:

    def __init__(self):
        self.all_locations = {"location":self.specific_location}

        self.specific_location = {"locations":None, "interactions":None, "npcs":None}

class Mottengard(Map):

    def __init__(self):
        
        # Map locations
        self.caravan = {"locations":["village square"], 
                        "interactions":{"use item":None, "exit":None}, 
                        "npcs":"No NPCs"}
        
        self.village_square = {"locations":["inn", "blacksmith", "general store", "training ground", "forest path"], 
                               "interactions":{"use item":None, "pet dog":self.dog_interaction, "exit":None}, 
                               "npcs":{"old man":mottengard_npcs["old man"], "villager":mottengard_npcs["villager vs"]}}
        
        self.blacksmith = {"locations":["village square"], 
                           "interactions":{"use item":None, "exit":None}, 
                           "npcs":{"blacksmith":mottengard_npcs["blacksmith"]}}
        
        self.training_ground = {"locations":["village square"], 
                                "interactions":{"use item":None, "combat":{"rookie trainer":mottengard_npcs["rookie trainer"]}, "cut tree":self.tree_interaction, "exit":None}, 
                                "npcs":{"rookie trainer":mottengard_npcs["rookie trainer"]}}
        
        self.general_store = {"locations":["village square"], 
                              "interactions":{"use item":None, "exit":None}, 
                              "npcs":{"general store trader":mottengard_npcs["general store trader"]}}
        
        self.inn = {"locations":["village square"], 
                    "interactions":{"use item":None, "access chest":self.chest_storage_inn, "exit":None}, 
                    "npcs":{"villager":mottengard_npcs["villager inn"], 
                            "local drunk":mottengard_npcs["local drunk"], 
                            "inn owner":mottengard_npcs["inn trader"]}}
        
        self.forest_path = {"locations":["village square"], 
                            "interactions":{"use item":None, "leave mottengard":self.exit, "exit":None}, 
                            "npcs": {"guard":mottengard_npcs["guard"]}}

        self.all_locations = {"caravan":self.caravan, 
                              "village square":self.village_square, 
                              "blacksmith":self.blacksmith, 
                              "inn":self.inn, 
                              "training ground":self.training_ground, 
                              "general store":self.general_store, 
                              "forest path":self.forest_path}
        
    def tree_interaction(self, character=None, active=False):
        if active:
            if item.stone_axe not in list(character.inventory.keys()):
                print("No axe to cut down tree!")
            elif item.stone_axe in list(character.inventory.keys()):
                print(f"You've cut down a tree!")
                character.use_item(item.stone_axe, interaction_type="non combat", object=item.training_ground_tree)

    def dog_interaction(self, character=None, active=False):
        if active:
            print("Dog: Woof! Woof!")

    def exit(self, character=None, active=False):
        if active:
            character.current_map = MythosForest()
            character.current_location = "forest entrance"
            character.location_data = character.current_map.all_locations[character.current_location]

    def chest_storage_inn(self, character=None, active=False):
        if active:
            
            character.view_inventory()
            items_stored = character.stored_items
            character.view_stored_items()

            storage_option = input("Do you want to withdraw items, store items or nothing?\n")
            while True:
                if storage_option == "withdraw":
                    if character.full_inventory:
                        print("Inventory full!")
                    elif character.stored_items_size == 0:
                        print("Storage is empty.")
                    else:
                        while True:
                            item_name = input("Type the name of the item or exit: ")

                            if item_name == "exit":
                                break
                            
                            if character.full_inventory:
                                print("Inventory full!")
                                break
                            elif character.stored_items_size == 0:
                                print("Storage is empty.")
                                break

                            if item_name not in list(item.all_items.keys()):
                                print("You typed an invalid item.")
                                continue


                            fetched_item = item.all_items[item_name]

                            if fetched_item not in list(items_stored.keys()):
                                print("You typed an invalid item.")
                            else:
                                character.pickup_item(fetched_item)
                                character.remove_from_stored(fetched_item)

                                print("Item withdrawn")

                                character.view_inventory()
                                character.view_stored_items()
                                print(f"Availabe Storage: {character.stored_items_size} / {character.max_stored_item_size}")
                                
                    break
                elif storage_option == "store":
                    if character.full_stored_items:
                        print("No more storage capacity!")
                    elif character.inventory_size == 0:
                        print("Inventory empty.")
                    else:
                        while True:
                            item_name = input("Type the name of the item or exit: ")
                            
                            if item_name == "exit":
                                break
                            
                            if character.full_stored_items:
                                print("No more storage capacity!")
                                break
                            elif character.inventory_size == 0:
                                print("Inventory empty.")
                                break

                            if item_name not in list(item.all_items.keys()):
                                print("You typed an invalid item.")
                                continue

                            fetched_item = item.all_items[item_name]

                            if fetched_item not in list(character.inventory.keys()):
                                print("You typed an invalid item.")
                            else:
                                character.drop_item(fetched_item)
                                character.place_into_storage(fetched_item)
                                print("Item stored.")
                            
                                character.view_inventory()
                                character.view_stored_items()
                                print(f"Availabe Storage: {character.stored_items_size} / {character.max_stored_item_size}")
                                
                    break
                elif storage_option == "nothing":
                    break
                else:
                    print("Type valid option.")
                    storage_option = input("Do you want to withdraw items, store items or nothing?\n")

class MythosForest(Map):

    def __init__(self):

        self.forest_entrance = {"locations":[""], 
                                "interactions":{"use item":None, "leave mythos forest":self.exit_mottengard}, 
                                "npcs": {}}
        
        self.all_locations = {"forest entrance":self.forest_entrance}


    def exit_mottengard(self, character=None, active=False):
        if active:
            character.current_map = Mottengard()
            character.current_location = "forest path"
            character.location_data = character.current_map.all_locations[character.current_location]

if __name__ == "__main__":

    from character import PlayerCharacter
    from quest import quest_database
    from item import stone_axe

    test_character = PlayerCharacter(base_health=15, base_attack=1, base_defence=0, level=1, current_map=Mottengard(), quest_database=quest_database)
    test_character.pickup_item(stone_axe)
    test_character.view_inventory()
    Mottengard().training_ground["interactions"]["cut tree"](character=test_character, active=True)
    test_character.view_inventory()

