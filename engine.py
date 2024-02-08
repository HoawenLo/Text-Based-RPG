import helper_functions
import item
import os
import pickle
import world
from quest import quest_database
from character import PlayerCharacter
from npc import mottengard_npcs

class Engine:

    def __init__(self):

        with open("load_new_game.txt", "r") as file:
            self.title_intro = file.read()

        self.title_screen = "Chronicles of Eldoria"
        self.options = ["play", "lore", "exit"]
        self.game_running = False

        # lore

        # exit
    
    def load_new_game(self):
        
        helper_functions.title_crawl(self.title_screen, text_speed=0.3)
        helper_functions.title_crawl(self.title_screen, text_speed=0.01)
        
        print(f"{self.title_screen}")

        helper_functions.text_crawl(self.title_intro, text_speed=0.1, line_length=60)

        self.character = PlayerCharacter(base_health=15, base_attack=1, base_defence=0, level=1, current_map=world.Mottengard(), quest_database=quest_database)

        if self.character.base_health == 15:
            print("character loaded successfully")

        self.character.current_location = "caravan"
        self.character.location_data = self.character.current_map.all_locations[self.character.current_location]

        self.character.pickup_item(item.all_items["basic map"])
        self.character.pickup_item(item.all_items["simple health potion"])
        self.character.pickup_item(item.all_items["apple"])
        self.character.pickup_item(item.all_items["stone axe"])

        welcome_text = "You arrive in Mottengard welcomed by an old man."
        helper_functions.text_crawl(welcome_text)

        tutorial_old_man = mottengard_npcs["tutorial man"]
        tutorial_old_man.run_dialogue(True)
        tutorial_old_man.character_reference = self.character
        tutorial_old_man.activate_quest()

    def handle_input(self):
        while self.game_running:
            print(f"current location: {self.character.current_location}")
            command = input("-- 1 move -- 2 interact -- 3 npcs -- 4 items -- 5 quests -- 6 stats -- 7 save and exit --\n")

            if command == "1":
                self.character.move()
                self.character.check_all_quests()
            elif command == "2":
                while True:
                    available_interactions = self.character.location_data["interactions"]
                    if available_interactions == "No interactions":
                        print(available_interactions)
                        break
                    else:
                        print("Available interactions: ", helper_functions.seperate_list(list(available_interactions.keys())))
                        interaction_command = input("Select interaction ")
                        if interaction_command == "combat":
                            available_npcs = available_interactions[interaction_command]
                            print(f"Available aggresive npcs: {helper_functions.seperate_list(list(available_npcs.keys()))}")
                            while True:
                                npc_response = input("Input npc name to fight\n")
                                if npc_response not in list(available_npcs.keys()):
                                    print("Invalid npc name.")
                                else:
                                    print(f"Combat started with {npc_response}")
                                    self.character.enter_combat(available_npcs[npc_response])
                                    break
                            if self.character.dead:
                                print("Game over!")
                                self.game_running =False
                            self.character.check_all_quests()
                            break
                        elif interaction_command == "use item":
                            all_inv_objs = list(self.character.inventory.keys())

                            available_tools = [inv_obj for inv_obj in all_inv_objs if inv_obj.item_type == "tool" or inv_obj.item_type == "consumable" ]

                            if len(available_tools) == 0:
                                print("No available tools.")
                                break
                            else:
                                print("Available tools:")
                                
                                for tool in available_tools:
                                    print(f"{tool.item_name}: {tool.item_description}")
                                tool_response = input("Input name of tool to use: ")
                                tool_fetch = item.all_items[tool_response]
                                if tool_fetch not in list(self.character.inventory.keys()):
                                    print("Item not in inventory!")
                                else:
                                    tool_fetch.execute_active_effect(character=self.character, active=True)
                                    print(f"{tool_fetch.item_name} used.")
                                    if tool_fetch.item_type == "consumable":
                                        self.character.drop_item(tool_fetch)
                            self.character.check_all_quests()
                        elif interaction_command == "exit":
                            break                        
                        elif interaction_command in list(available_interactions.keys()):
                            self.character.location_data["interactions"][interaction_command](character=self.character, active=True)
                            self.character.check_all_quests()
                            break
                        else:
                            print("Invalid interaction suggested. Type a valid number.")
            elif command == "3":
                while True:
                    if self.character.location_data["npcs"] == "No NPCs":
                        print(self.character.location_data["npcs"])
                        break
                    else:
                        available_npcs = helper_functions.seperate_list(list(self.character.location_data["npcs"].keys()))
                        print(f"Available npcs: {available_npcs} , type none if no interaction wanted")
                        npcs_command = input("Interact with npc: ")

                        if npcs_command == "none":
                            break
                        elif npcs_command in available_npcs:

                            fetched_npc = self.character.location_data["npcs"][npcs_command]
                            if fetched_npc.npc_type == "normal":
                                fetched_npc.run_dialogue(True)
                            if fetched_npc.npc_type == "quest":
                                fetched_npc.run_dialogue(True)
                                fetched_npc.character_reference = self.character
                                fetched_npc.activate_quest()
                            if fetched_npc.npc_type == "trader":
                                fetched_npc.character_reference = self.character
                                fetched_npc.run_trading_dialogue(True)
                            self.character.check_all_quests()
                        else:
                            print("NPC does not exist.")

            elif command == "4":
                while True:
                    inventory_command = input("Select to view -- inventory -- equipped -- exit --\n")
                    if inventory_command == "inventory":
                        self.character.view_inventory()
                        print(f"Gold: {self.character.gold}")
                        print(f"Inventory space: {self.character.inventory_size} / {self.character.max_inventory_size}")
                        if len(self.character.inventory) > 0:
                            while True:
                                drop_items = input("Would you like to drop any items? yes/no\n")
                                if drop_items == "yes":
                                    drop_item_name = input("Type item name: ")
                                    if drop_item_name not in list(item.all_items.keys()):
                                        print("Item does not exist. Perhaps you typed it incorrectly?")
                                    else:
                                        self.character.drop_item(item.all_items[drop_item_name])
                                        self.character.view_inventory()
                                elif drop_items == "no":
                                    break
                                else:
                                    print("Type yes or no")
                    elif inventory_command == "equipped":
                        self.character.view_equipped()
                        while True:
                            equip_commands = input("Would you like to equip items, unequip items or exit?\n")
                            if equip_commands == "equip":
                                self.character.show_equippable()
                                equip_item_name = input("Type item name: ")
                                if equip_item_name not in list(item.all_items.keys()):
                                    print("Item does not exist. Perhaps you typed it incorrectly?")
                                else:
                                    self.character.equip_item(item.all_items[equip_item_name])
                                    self.character.view_equipped()
                                    self.character.view_stats()
                                    self.character.check_all_quests()
                            elif equip_commands == "unequip":
                                equip_item_name = input("Type item name: ")
                                if equip_item_name not in list(item.all_items.keys()):
                                    print("Item does not exist. Perhaps you typed it incorrectly?")
                                else:                    
                                    self.character.unequip_item(item.all_items[equip_item_name])
                                    self.character.view_equipped()
                                    self.character.view_stats()
                            elif equip_commands == "exit":
                                break
                            else:
                                print("Type equip / unequip / exit")
                    elif inventory_command == "exit":
                        break
            elif command == "5":
                while True:
                    quest_command = input ("View: -- completed -- incomplete -- exit --\n")
                    if quest_command == "completed":
                        self.character.view_completed_quests()
                    elif quest_command == "incomplete":
                        self.character.view_incompleted_quests()
                    elif quest_command == "exit":
                        break
            elif command == "6":
                self.character.view_stats()
            elif command == "7":
                self.game_running = False
                self.save_game("savegame.pkl")
                break

    def load_title_screen(self):
        helper_functions.title_crawl(self.title_screen, text_speed=0.3)
        
        print(f"{self.title_screen}")

    # Version one
    
    def save_game(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.character, file)
        print("Game saved!")

    def load_game(self, filename):
        with open(filename, "rb") as file:
            loaded_game = pickle.load(file)
        return loaded_game

    def run_game(self):
        first_loading = True
        while True:

            if first_loading:
                self.load_title_screen()
                first_loading = False

            option = input(f"Select option: -- play -- lore -- exit --\n")

            if option not in self.options:
                print("type play / lore / exit")

            if option == "play":

                if os.path.isfile("savegame.pkl"):

                    while True:
                        response= input("Start a new game? yes/no\n")

                        if response == "yes":
                            self.game_running = True
                            self.load_new_game()
                            self.handle_input()
                            break
                        elif response == "no":
                            self.character = self.load_game("savegame.pkl")
                            self.game_running = True
                            self.handle_input()
                            break
                        else:
                            print("Type yes or no.")
                else:
                    self.game_running = True
                    self.load_new_game()
                    self.handle_input()
                    
            elif option == "lore":
                print("Nothing here yet.")
            elif option == "exit":
                break



if __name__ == "__main__":
    pass
    # test_character = PlayerCharacter(base_health=15, base_attack=1, base_defence=0, level=1, current_map=world.Mottengard())
    
    # if test_character.health == 15:
    #     print("character loaded successfully")

    # test_item_one = item.simple_copper_chestplate
    # test_item_two = item.simple_copper_sword

    # test_character.pickup_item(test_item_one)
    # test_character.pickup_item(test_item_two)

    # print("test character inventory:", test_character.inventory)

    # while True:
    #     inventory_command = input("Select to view -- inventory -- equipped -- exit --\n")
    #     if inventory_command == "inventory":
    #         test_character.view_inventory()
    #         if len(test_character.inventory) > 0:
    #             while True:
    #                 drop_items = input("Would you like to drop any items? yes/no\n")
    #                 if drop_items == "yes":
    #                     drop_item_name = input("Type item name: ")
    #                     if drop_item_name not in list(item.all_items.keys()):
    #                         print("Item does not exist. Perhaps you typed it incorrectly?")
    #                     else:
    #                         test_character.drop_item(item.all_items[drop_item_name])
    #                         test_character.view_inventory()
    #                 elif drop_items == "no":
    #                     break
    #                 else:
    #                     print("Type yes or no")
    #     elif inventory_command == "equipped":
    #         test_character.view_equipped()
    #         while True:
    #             equip_commands = input("Would you like to equip items, unequip items or exit?\n")
    #             if equip_commands == "equip":
    #                 test_character.show_equippable()
    #                 equip_item_name = input("Type item name: ")
    #                 if equip_item_name not in list(item.all_items.keys()):
    #                     print("Item does not exist. Perhaps you typed it incorrectly?")
    #                 else:
    #                     test_character.equip_item(item.all_items[equip_item_name])
    #                     test_character.view_equipped()
    #             elif equip_commands == "unequip":
    #                 equip_item_name = input("Type item name: ")
    #                 if equip_item_name not in list(item.all_items.keys()):
    #                     print("Item does not exist. Perhaps you typed it incorrectly?")
    #                 else:                    
    #                     test_character.unequip_item(item.all_items[equip_item_name])
    #                     test_character.view_equipped()
    #             elif equip_commands == "exit":
    #                 break
    #             else:
    #                 print("Type equip / unequip / exit")
    #     elif inventory_command == "exit":
    #         break