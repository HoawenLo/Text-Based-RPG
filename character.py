from random import randint
import item as itm

class PlayerCharacter:

    def __init__(self, base_health, base_attack, base_defence, level, current_map, quest_database):
        self.current_health = base_health
        self.base_health = base_health
        self.attack = base_attack
        self.defence = base_defence
        
        self.level = level
        self.current_exp = 0
        self.level_limit = 50
        
        self.current_location = ""
        self.current_map = current_map
        self.location_data = {}

        self.gold = 100

        self.inventory = {}
        self.inventory_size = 0
        self.max_inventory_size = 10
        self.full_inventory = False

        self.stored_items = {}
        self.stored_items_size = 0
        self.max_stored_item_size = 5
        self.full_stored_items = False

        self.equipped_helmet = None
        self.equipped_chestplate = None
        self.equipped_weapon = None
        self.equipped_ring = None

        self.quest_database = quest_database
        self.completed_quest_list = {}
        self.incompleted_quest_list = {}

        self.defeated_npcs = {}
        self.in_combat = False
        self.dead = False

        self.active_dialogue_npc = None



    # Movement
        
    def move(self):
        list_locations = ""

        for location in self.location_data["locations"]:
            list_locations += f" -- {location}"

        list_locations += " --"

        print(f"Available locations: {list_locations}")

        next_location = input("Move to ")
        
        if next_location not in self.location_data["locations"]:
            print("Invalid location.")
        else:
            self.current_location = next_location
            self.location_data = self.current_map.all_locations[self.current_location]

    # Combat

    def enter_combat(self, target):
        while True:
            print(f"Your health: {self.current_health}, Enemy Remaining health: {target.health}, Enemy level: {target.skill_level}")
            combat_response = input("Select options: attack / item / run\n")
            if combat_response == "attack":
                damage_inflicted = self.attack_target(target)
                print(f"You attack and deal {damage_inflicted} damage.")
                if target.health <= 0:
                    print("You have won the battle!")
                    exp_range = target.exp_output
                    exp_reward = randint(exp_range[0], exp_range[1])
                    print(f"{exp_reward} exp gained.")
                    self.gain_exp(exp_reward)

                    gold_range = target.gold_range
                    gold_reward = randint(gold_range[0], gold_range[1])
                    print(f"{gold_reward} Gold gained")
                    self.gold += gold_reward
                    break
                damage_taken = self.defend_target(target)
                print(f"The enemy deals {damage_taken} damage.")
                if self.current_health <= 0:
                    print("You have died!")
                    self.dead = True
                    break
            elif combat_response == "item":
                while True:
                    self.view_inventory()
                    item_response = input("Type item name / exit\n")

                    if item_response == "exit":
                        break

                    if item_response not in list(itm.all_items.keys()):
                        print("Invalid item.")
                    else:
                        self.use_item(itm.all_items[item_response], interaction_type="combat")
            elif combat_response == "run":
                random_number = randint(1,3)
                if random_number == 1:
                    print("Succesfully escape!")
                    break
                else:
                    print("Failed to escape.")
            else:
                print("Invalid command.")

    def attack_target(self, target):

        if target.skill_level > 5:
            offset_value = randint(1, 5)
            damage = self.attack - target.defence - offset_value 

        elif target.skill_level < 5:
            offset_value = randint(0,3)
            damage = self.attack - target.defence - offset_value

        damage = self.attack - target.defence
        target.health -= damage

        if target.health <= 0:
            if target not in self.defeated_npcs.keys():
                self.defeated_npcs[target] = 1
            else:
                self.defeated_npcs[target] += 1

        return damage
        
    def defend_target(self, target):
        
        offset_value = randint(0, 3)

        if target.skill_level > 3:
            damage = target.attack - self.defence + offset_value
        else:
            damage = target.attack - self.defence - offset_value

        if damage < 0:
            damage = 0

        self.current_health -= damage

        return damage

    def use_item(self, item, interaction_type, **kwargs):
        
        if interaction_type == "combat":
            if item not in self.inventory:
                print("You selected an invalid item.")
            else:
                item.execute_active_effect(character=self)
                self.drop_item(item)
        elif interaction_type == "non combat":
            
            item.execute_active_effect(character=self, kwargs=kwargs)
            
            if item.item_type == "consumable":
                self.drop_item(item)

    def gain_exp(self, exp):
        if self.level == 20:
            print("Max level reached.")
        elif self.level < 20:
            self.current_exp += exp
            if self.current_exp > self.level_limit:
                self.level += 1

                if self.level == 5:
                    attack_gained = 6
                    defence_gained = 1
                    health_gained = 1
                    self.base_health += health_gained
                    self.attack += attack_gained
                    self.defence += defence_gained
                    self.level_limit = (2 ** self.level) * 50
                    self.current_exp = 0
                    print(f"Levelled up! Gained {health_gained} health, {attack_gained} attack and {defence_gained} defence.")                    
                elif self.level == 10:
                    attack_gained = 10
                    defence_gained = 2
                    health_gained = 2
                    self.base_health += health_gained
                    self.attack += attack_gained
                    self.defence += defence_gained
                    self.level_limit = (2 ** self.level) * 50
                    self.current_exp = 0
                    print(f"Levelled up! Gained {health_gained} health, {attack_gained} attack and {defence_gained} defence.")                    
                elif self.level == 15:
                    attack_gained = 15
                    defence_gained = 4
                    health_gained = 4
                    self.base_health += health_gained
                    self.attack += attack_gained
                    self.defence += defence_gained
                    self.level_limit = (2 ** self.level) * 50
                    self.current_exp = 0
                    print(f"Levelled up! Gained {health_gained} health, {attack_gained} attack and {defence_gained} defence.")                    
                elif self.level == 20:
                    attack_gained = 25
                    defence_gained = 8
                    health_gained = 8
                    self.base_health += health_gained
                    self.attack += attack_gained
                    self.defence += defence_gained
                    self.level_limit = (2 ** self.level) * 50
                    self.current_exp = 0
                    print(f"Levelled up! Gained {health_gained} health, {attack_gained} attack and {defence_gained} defence.")                    
                else:
                    health_gained = 3
                    self.base_health += health_gained
                    self.level_limit = (2 ** self.level) * 50
                    self.current_exp = 0
                    print(f"Levelled up! Gained {health_gained}.")


    # Inventory
    
    def view_inventory(self):
        
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

    def view_stored_items(self):
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
        

    def pickup_item(self, item):

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
        
        if item not in self.inventory.keys():
            print("Item not in inventory!")
        else:
            if self.inventory[item] > 0:
                self.inventory[item] -= 1
                self.inventory_size -= 1
                self.full_inventory = False

            if self.inventory[item] == 0:
                del self.inventory[item]
    
    def remove_from_stored(self, item):

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

    def view_equipped(self):

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

    def show_equippable(self):

        if len(self.inventory.keys()) == 0:
            print("Inventory empty.")
        else:
            equippable_items = ["helmet", "chestplate", "weapon", "ring"]

            print("Equipable:")
            for item in self.inventory.keys():

                if item.item_type in equippable_items:
                    print(f"{item.item_name} : {item.item_type}")

    # Equip items
            
    def equip_item(self, item):

        if item not in self.inventory.keys():
            print("Item not in inventory.")
        else:
            if item.item_type == "helmet" and self.equipped_helmet == None:
                self.equipped_helmet = item
                self.drop_item(item)
                self.attack += self.equipped_helmet.attack
                self.defence += self.equipped_helmet.defence

                self.equipped_helmet.execute_passive_effect(self, equip_flag=True)

            elif item.item_type == "helmet" and self.equipped_helmet != None:
                print("Unequip item first!")
                    
            if item.item_type == "chestplate" and self.equipped_chestplate == None:
                self.equipped_chestplate = item
                self.drop_item(item)
                self.attack += self.equipped_chestplate.attack
                self.defence += self.equipped_chestplate.defence

                self.equipped_chestplate.execute_passive_effect(self, equip_flag=True)
                
            elif item.item_type == "chestplate" and self.equipped_chestplate != None:
                print("Unequip item first!")

            if item.item_type == "weapon" and self.equipped_weapon == None:
                self.equipped_weapon = item
                self.drop_item(item)
                self.attack += self.equipped_weapon.attack
                self.defence += self.equipped_weapon.defence

                self.equipped_weapon.execute_passive_effect(self, equip_flag=True)

            elif item.item_type == "weapon" and self.equipped_weapon != None:
                print("Unequip item first!")

            if item.item_type == "ring" and self.equipped_ring == None:
                self.equipped_ring = item
                self.drop_item(item)
                self.attack += self.equipped_ring.attack
                self.defence += self.equipped_ring.defence
                
                self.equipped_ring.execute_passive_effect(self, equip_flag=True)

            elif item.item_type == "ring" and self.equipped_ring != None:
                print("Unequip item first!")

    def unequip_item(self, item):
        if self.full_inventory == True:
            print("Inventory is full!")

        if item.item_type == "helmet" and self.equipped_helmet == None:
            print("Nothing equipped!")
        elif item.item_type == "helmet" and self.equipped_helmet != None and self.full_inventory == False:
            self.pickup_item(item)

            self.attack -= self.equipped_helmet.attack
            self.defence -= self.equipped_helmet.defence

            self.equipped_helmet = None
            
            item.execute_passive_effect(self, equip_flag=False)

        if item.item_type == "chestplate" and self.equipped_chestplate == None:
            print("Nothing equipped!")
        elif item.item_type == "chestplate" and self.equipped_chestplate != None and self.full_inventory == False:
            self.pickup_item(item)

            self.attack -= self.equipped_chestplate.attack
            self.defence -= self.equipped_chestplate.defence

            self.equipped_chestplate = None

            item.execute_passive_effect(self, equip_flag=False)

        if item.item_type == "weapon" and self.equipped_weapon == None:
            print("Nothing equipped!")
        elif item.item_type == "weapon" and self.equipped_weapon != None and self.full_inventory == False:
            self.pickup_item(item)                
            
            self.attack -= self.equipped_weapon.attack
            self.defence -= self.equipped_weapon.defence

            self.equipped_weapon = None

            item.execute_passive_effect(self, equip_flag=False)
            

        if item.item_type == "ring" and self.equipped_ring == None:
            print("Nothing equipped!")            
        elif item.item_type == "ring" and self.equipped_ring != None and self.full_inventory == False:
            self.pickup_item(item)                
            
            self.attack -= self.equipped_ring.attack
            self.defence -= self.equipped_ring.defence

            self.equipped_ring = None

            item.execute_passive_effect(self, equip_flag=False)


    # Interactions

    def buy_items(self, item):
        
        if self.gold - item.value >= 0:
            if self.full_inventory == False:
                self.pickup_item(item)
                self.gold -= item.value
                print(f"{item.item_name} purchased.")
                print(f"Gold: {self.gold}")
                return True
            elif self.full_inventory == True:
                print("Inventory is full!")
        else:
            print("Not enough gold!")

    # Quests
                
    def view_completed_quests(self):

        if self.completed_quest_list == {}:
            print("Empty.")

        for quest_name, quest_data in self.completed_quest_list.items():
            quest_reward = quest_data
            print(f"{quest_name} : {quest_reward}")

    def view_incompleted_quests(self):

        if self.incompleted_quest_list == {}:
            print("Empty.")

        for quest_name, quest_data in self.incompleted_quest_list.items():
            quest_instruction = quest_data
            print(f"{quest_name} : {quest_instruction}")

    def add_quest(self, quest_reference):
        # make sure not in completed
        fetched_quest = self.quest_database[quest_reference]
        fetched_quest.character = self
        fetched_quest.activate_quest = True
        fetched_quest.run_quest()
        self.incompleted_quest_list[quest_reference] = fetched_quest.current_goal

    def update_quest(self, quest_reference):
        fetched_quest = self.quest_database[quest_reference]
        if fetched_quest.complete == False:
            fetched_quest.run_quest()
            if fetched_quest.complete:
                del self.incompleted_quest_list[quest_reference]
                self.completed_quest_list[quest_reference] = fetched_quest.rewards
            else:
                self.incompleted_quest_list[quest_reference] = fetched_quest.current_goal

    def check_all_quests(self):
        if len(list(self.incompleted_quest_list.keys())) == 0:
            pass
        else:
            for quest_name in list(self.incompleted_quest_list.keys()):
                self.update_quest(quest_name)

    # view stats
        
    def view_stats(self):
        print(f"Level: {self.level}")
        print(f"Health: {self.current_health} / {self.base_health}")
        print(f"Attack: {self.attack}")
        print(f"Defence: {self.defence}")
        print(f"Current Experience: {self.current_exp}/{self.level_limit}")
    


if __name__ == "__main__":

    import world
    import quest
    import item

    test_character = PlayerCharacter(base_health=10, base_attack=1, base_defence=0, level=1, current_map=world.Mottengard(), quest_database=quest.quest_database)

    test_character.pickup_item(item.all_items["warrior's ring"])
    input("")
    test_character.view_stats()
    test_character.view_equipped()
    input("")
    test_character.equip_item(item.all_items["warrior's ring"])
    test_character.view_stats()
    test_character.view_equipped()
    input("")
    test_character.unequip_item(item.all_items["warrior's ring"])
    test_character.view_stats()
    test_character.view_equipped()
