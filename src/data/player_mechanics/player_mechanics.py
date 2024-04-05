import sys
import os

from random import randint

from ...text_manipulation.text_manipulation import *

class Player:

    # ------------- Player attributes ------------- #

    def __init__(self, base_health, base_attack, base_defence, level, current_location):

        # ------------- stats ------------- #

        self.current_health = base_health
        self.base_health = base_health
        self.attack = base_attack
        self.defence = base_defence

        # ------------- level ------------- #

        self.level = level
        self.current_exp = 0
        self.level_limit = 50
        
        # ------------- location ------------- #

        self.current_area = ""
        self.current_location = current_location
        self.area_data = {}

        # ------------- inventory ------------- #

        self.gold = 100

        self.inventory = {}
        self.inventory_size = 0
        self.max_inventory_size = 10
        self.full_inventory = False

        # ------------- stored_items ------------- #

        self.stored_items = {}
        self.stored_items_size = 0
        self.max_stored_item_size = 5
        self.full_stored_items = False

        # ------------- equipped items ------------- #

        self.equipped_helmet = None
        self.equipped_chestplate = None
        self.equipped_weapon = None
        self.equipped_ring = None

        # ------------- quests ------------- #

        self.completed_quest_list = {}
        self.ongoing_quest_list = {}

        self.defeated_npcs = {}
        
        # ------------- combat ------------- #

        self.in_combat = False
        self.dead = False

    # ------------- Player mechanics ------------- #

    # ------------- movement ------------- #
        
    def move(self):
        """Move the character to a new area.

        Pull the list of areas that the player can move to.
        List the areas.
        Take player response on where to move to.
        
        Args:
            None
            
        Returns:
            None"""
        available_areas = self.area_data["areas"]

        list_areas = ""

        for i, area in available_areas.items():
            list_areas += f" -- {i} {remove_underscore(area)}"

        list_areas += " --"

        print(f"Available areas: {list_areas}")

        next_area_num = input("Move to (type number) ")
        
        if next_area_num not in available_areas.keys():
            print("Invalid area.")
        elif available_areas[next_area_num] == "Cancel":
            pass
        else:
            self.current_area = available_areas[next_area_num]

            print(self.current_location[available_areas[next_area_num]])
            self.area_data = self.current_location[available_areas[next_area_num]]

    # ------------- inventory ------------- #
    
    def view_inventory(self):
        """View all items in inventory."""
        if len(self.inventory.keys()) == 0:
            print("Inventory empty.")
        else:
            print("Inventory:")
            for item, item_number in self.inventory.items():
                if item.item_stack:
                    print(f"{item_number} x {item.item_name}")
                else:
                    for _ in range(item_number):
                        print(f"1 x {item.item_name}")

    

    def pickup_item(self, item):
        """Pickup item to store in inventory.
        
        Args:
            item: The item object to pickup into inventory."""
        if self.full_inventory == True:
            print("Inventory full!")
        
        if item not in self.inventory.keys() and self.full_inventory == False:
            self.inventory[item] = 1
            self.inventory_size += 1
            if self.inventory_size == self.max_inventory_size:
                self.full_inventory = True
        elif self.full_inventory == False:
            self.inventory[item] += 1
            self.inventory_size += 1
            if self.inventory_size == self.max_inventory_size:
                self.full_inventory = True

    def drop_item(self, item):
        """Drop item from the inventory.
        
        Args:
            item: The item object to drop from inventory."""
        if item not in self.inventory.keys():
            print("Item not in inventory!")
        else:
            if self.inventory[item] > 0:
                self.inventory[item] -= 1
                self.inventory_size -= 1
                self.full_inventory = False

            if self.inventory[item] == 0:
                del self.inventory[item]
    
    def drop_items_section(self, item_database):
        """Run a while loop to drop items.
        
        Args:
            item_database: The item database to access all item values.
            
        Returns:
            None"""

        drop_items = input("Would you like to drop items?\n -- 1 yes -- 2 no -- \nResponse: ")
        while True:
            if drop_items == "1":
                drop_item_name = input("Type item name: ")
                if drop_item_name not in list(item_database.keys()):
                    print("Item does not exist. Perhaps you typed it incorrectly?")
                else:
                    self.drop_item(item_database[drop_item_name])
                    self.view_inventory()
            elif drop_items == "2":
                break
            else:
                print("Type 1 or 2.")


    def run_inventory_interaction(self, item_database):
        """Run the inventory interaction to view inventory
        or drop items in the inventory.
        
        Args:
            item_database: The item database to access all item values.
            
        Returns:
            None"""
        
        self.view_inventory()
        if len(self.inventory.keys()) != 0:
            self.drop_items_section(item_database)

    def buy_item(self, item):
        """Character interaction to buy item.
        
        Args:
            item: The item object stored in the item database.
            
        Returns:
            None"""
        if self.gold - item.value >= 0:
            print("Not enough gold!")
        elif self.full_inventory == True:
            print("Inventory is full!")
        else:
            self.pickup_item(item)
            self.gold -= item.value
            print(f"{item.item_name} purchased.")
            print(f"Gold: {self.gold}")

    def sell_item(self, item):
        """Character interaction to sell item.
        
        Args:
            item: The item object stored in the item database.
            
        Returns:
            None"""
         
        if item.item_name not in self.inventory.keys():
            print("Invalid item typed.")
        else:
            self.drop_item(item)
            self.gold += item.value
            print(f"{item.item_name} sold.")
            print(f"Gold: {self.gold}")
    

    # ------------- Using items ------------- #
                
    def get_available_tools(self, sit_type):
        """Get available tools; items which can be used.
        
        Args:
            sit_type: The situation type. Either combat or
            non combat. Combat can use only consumables.

        Returns:
            List of available tools; items which can be used."""

        all_items = list(self.inventory.keys())

        available_tools = []

        if sit_type == "combat":
            tool_search_cond = (item.item_type == "consumable")
        elif sit_type == "non combat":
            tool_search_cond = (item.item_type == "tool" or item.item_type == "consumable")

        for item in all_items:
            if tool_search_cond:
                available_tools.append(item)
        
        return available_tools

    def run_use_item_menu(self, item_database):
        """Run the use item menu for combat or non combat
        situations."""

        available_tools = self.get_available_tools()

        if len(available_tools) == 0:
            print("No available tools.")
        else:
            print("Available tools:")
                                
            for tool in available_tools:
                print(f"{tool.item_name}: {tool.item_description}")
            tool_response = input("Input name of tool to use: ")
            tool_fetch = item_database[tool_response]

            self.use_item(tool_fetch)

    def use_item(self, item):
        """Use item in combat or non combat situation.
        
        Args:
            item: The item object to use."""
        if item not in self.inventory:
            print("You selected an invalid item.")
        else:
            item.execute_active_effect(character=self)

            if item.item_type == "consumable":
                self.drop_item(item)

    # ------------- Stored items ------------- #

    def view_stored_items(self):
        """View stored items."""
        if len(self.stored_items.keys()) == 0:
            print("No stored items.")
        else:
            print("Stored items:")
            for item, item_number in self.stored_items.items():
                if item.item_stack:
                    print(f"{item_number} x {item.item_name}")
                else:
                    for _ in range(item_number):
                        print(f"1 x {item.item_name}")

    def remove_from_stored(self, item):
        """Remove item from storage.
        
        Args:
            item: The item object to remove from storage."""
        if item not in self.stored_items.keys():
            print("Item not in stored items!")
        else:
            if self.stored_items[item] > 0:
                self.stored_items[item] -= 1
                self.stored_items_size -= 1
                self.full_stored_items = False

            if self.stored_items[item] == 0:
                del self.stored_items[item]

    def place_into_storage(self, item):
        """Place item from storage.
        
        Args:
            item: The item object to put into storage."""
        if self.full_stored_items == True:
            print("No space in stored items!")
        
        if item not in self.stored_items.keys() and self.full_stored_items == False:
            self.stored_items[item] = 1
            self.stored_items_size += 1
            if self.stored_items_size == self.max_stored_item_size:
                self.full_stored_items = True
        elif self.full_stored_items == False:
            self.stored_items[item] += 1
            self.stored_items_size += 1
            if self.stored_items_size == self.max_stored_item_size:
                self.full_stored_items = True

    # ------------- Equipped items ------------- #
                
    def show_equippable(self):
        """Show equippable items."""

        if len(self.inventory.keys()) == 0:
            print("Inventory empty.")
        else:
            equippable_items = ["helmet", "chestplate", "weapon", "ring"]

            print("Equipable:")
            for item in self.inventory.keys():

                if item.item_type in equippable_items:
                    print(f"{item.item_name} : {item.item_type}")

    def equip_item(self, item):
        """Equip item adding passive effects and stats.
        
        Args:
            item: The item to equip."""
        
        if item not in self.inventory.keys():
            print("Item not in inventory")
        else:
            item_type = item.item_type

            if item_type == "helmet":
                equipped_item = self.equipped_helmet
            elif item_type == "chestplate":
                equipped_item = self.equipped_chestplate
            elif item_type == "weapon":
                equipped_item = self.equipped_weapon
            elif item_type == "ring":
                equipped_item = self.equipped_ring

            if equipped_item == None:
                equipped_item = item
                self.drop_item(item)
                self.attack += self.equipped_item.attack
                self.defence += self.equipped_item.defence

                self.equipped_item.execute_passive_effect(self, equip_flag=True)
            elif equipped_item != None:
                print("Unequip item first!")
        
    def unequip_item(self, item):
        """Unequip item from inventory, removing the passive effects applied
        and stats.
        
        Args:
            item: The equipped item to be removed."""
        if self.full_inventory == True:
            print("Inventory is full!")

        item_type = item.item_type

        if item_type == "helmet":
            equipped_item = self.equipped_helmet
        elif item_type == "chestplate":
            equipped_item = self.equipped_chestplate
        elif item_type == "weapon":
            equipped_item = self.equipped_weapon
        elif item_type == "ring":
            equipped_item = self.equipped_ring

        if equipped_item == None:
            print("Nothing equipped!")
        elif equipped_item != None and self.full_inventory == False:
            self.pickup_item(item)

            self.attack -= self.equipped_helmet.attack
            self.defence -= self.equipped_helmet.defence

            equipped_item = None
            
            item.execute_passive_effect(self, equip_flag=False)

    def view_equipped(self):
        """Show equipped items after equipping or unequipping.
        
        Args:
            None
        
        Returns:
            None"""

        if self.equipped_helmet != None:
            helmet_name = self.equipped_helmet.item_name
        else:
            helmet_name = None

        if self.equipped_chestplate != None:
            chestplate_name = self.equipped_chestplate.item_name
        else:
            chestplate_name = None

        if self.equipped_weapon != None:
            weapon_name = self.equipped_weapon.item_name
        else:
            weapon_name = None

        if self.equipped_ring != None:
            ring_name = self.equipped_ring.item_name
        else:
            ring_name = None

        print("Equipped Items:")
        print(f"Helmet: {helmet_name}")
        print(f"Chestplate: {chestplate_name}")
        print(f"Weapon: {weapon_name}")
        print(f"Ring: {ring_name}")

    def check_equipped_empty(self):
        """Check if equipped item are empty."""

        equipped_items = [self.equipped_helmet, self.equipped_chestplate, self.equipped_weapon, self.equipped_ring]
        counter = 0

        for item in equipped_items:
            if item == None:
                counter += 1

        if counter == 4:
            return True
        else:
            return False

    def equip_logic(self, item_database):
        """Run the equip logic.
        
        Args:
            item_database: The item database to refer to all existing items.
            
        Returns:
            None"""
        self.view_equipped()
        if len(self.inventory.keys()) != 0:
            self.show_equippable()
            equip_item_name = input("Type item name: ")
            if equip_item_name not in list(item_database.keys()):
                print("Item does not exist. Perhaps you typed it incorrectly?")
            else:
                self.equip_item(item_database[equip_item_name])
                self.view_equipped()
                self.view_stats()
        else:
            print("Inventory empty.")

    def unequip_logic(self, item_database):
        """Run unequip logic.
        
        Args:
            item_database: The item database to refer to all existing items.
            
        Returns:
            None"""
        self.view_equipped()
        equipped_check = self.check_equipped_empty()
        if equipped_check:
            print("No items equipped.")
        else:
            equip_item_name = input("Type item name: ")
            if equip_item_name not in list(item_database.keys()):
                print("Item does not exist. Perhaps you typed it incorrectly?")
            else:                    
                self.unequip_item(item_database[equip_item_name])
                self.view_equipped()
                self.view_stats()

    def run_equip_interaction(self, item_database):
        """Run equip items interaction. 
        
        Args:
            None
            
        Returns:
            None"""
        
        while True:
            equip_command = input("-- 1 equip items -- 2 unequip items -- 3 exit --\nResponse: ")
            if equip_command == "1":
                self.equip_logic(item_database)
            elif equip_command == "2":
                self.unequip_logic(item_database)
            elif equip_command == "3":
                break
            else:
                print("Type 1, 2 or 3.")

    # ------------- Quests ------------- #
            
    def view_completed_quests(self):
        """View completed quests."""

        if self.completed_quest_list == {}:
            print("Empty.")

        for quest_name, quest_data in self.completed_quest_list.items():
            quest_reward = quest_data
            print(f"{quest_name} : {quest_reward}")

    def view_ongoing_quests(self):
        """View ongoing quests and descriptions."""
        if self.ongoing_quest_list == {}:
            print("Empty.")

        for quest_name, quest_data in self.ongoing_quest_list.items():
            quest_instruction = quest_data
            print(f"{quest_name} : {quest_instruction}")

    def add_quest(self, quest_reference):
        # make sure not in completed
        fetched_quest = self.quest_database[quest_reference]
        fetched_quest.character = self
        fetched_quest.activate_quest = True
        fetched_quest.run_quest()
        self.incompleted_quest_list[quest_reference] = fetched_quest.current_goal

    # ------------- Viewing stats ------------- #

    def view_stats(self):
        """View stats.
        
        Args:
            None
            
        Returns:
            None"""
        
        print(f"Level: {self.level}")
        print(f"Health: {self.current_health} / {self.base_health}")
        print(f"Attack: {self.attack}")
        print(f"Defence: {self.defence}")
        print(f"Current Experience: {self.current_exp}/{self.level_limit}")

if __name__ == "__main__":

    test = Player(base_health=15, 
                  base_attack=0, 
                  base_defence=0, 
                  level=0, 
                  current_location="test")
    
    test.area_data = {"areas":{"1":"test_one", "2":"test_two"}}

    test.move()
