from helper_functions import add_adventurer, text_crawl
import item
import quest


class Npc:

    def __init__(self, health, base_health, attack, defence, npc_type, dialogue):
        self.health = health
        self.base_health = base_health
        self.attack = attack
        self.defence = defence
        self.npc_type = npc_type

        self.dialogue_text = dialogue

    def run_dialogue(self, dialogue_active, quest_reference=None):
        if quest_reference == None:
            if callable(self.dialogue_text):
                self.dialogue_text(dialogue_active)
            else:
                return "Dialogue error."
        else:
            self.dialogue_text(dialogue_active, quest_reference=quest_reference)

class Quest(Npc):

    def __init__(self, health, base_health, attack, defence, npc_type, dialogue, quest_reference):
        super().__init__(health, base_health, attack, defence, npc_type, dialogue)

        self.quest_reference = quest_reference
        self.character_reference = None

    def activate_quest(self):
        
        self.character_reference.add_quest(self.quest_reference)

class Trader(Npc):

    def __init__(self, health, base_health, attack, defence, npc_type, dialogue, items):
        super().__init__(health, base_health, attack, defence, npc_type, dialogue)

        self.items = items
        self.character_reference = None

    def show_items(self):

        for item in self.items.values():
            print(f"{item.item_name} : {item.item_description} : {item.value} gold")

    def calculate_item_values(self, inventory_items):
        print("Items that can be sold: ")
        for inventory_item in inventory_items:
            print(f"{inventory_item.item_name} : {inventory_item.value // 2} g")

    
    def run_trading_dialogue(self, dialogue_active):
        self.dialogue_text(dialogue_active, self.show_items, self.character_reference, self.items, self.calculate_item_values)

    

class Aggresive(Npc):

    def __init__(self, health, base_health, attack, defence, npc_type, dialogue, skill_level, common_exp_ranges):
        super().__init__(health, base_health, attack, defence, npc_type, dialogue)

        self.skill_level = skill_level
        self.exp_ranges = common_exp_ranges
        self.exp_output = self.exp_ranges[self.skill_level]
        self.gold_range = (int((1.5 ** self.skill_level - 1) * 2), int((1.5 ** self.skill_level) * 2))

def mottengard_old_man_dialogue(dialogue_active):
    if dialogue_active:
        a_dialogue = ["Old man: Ah, a newcomer to Mottengard! I sense the spark of adventure in your eyes. Welcome, young one. What brings you to our humble village?" ]
        a_response = ["Adventurer: Thank you, sir. I've come in search of renown and fortune. There's talk of a grand quest and an ancient artifact."]
        
        a_a_dialogue = ["Old man: The Heartstone, no doubt. A tale as old as time. Many have sought it, but few truly understand its mysteries. Be cautious, for the path to Astralhaven is fraught with challenges."]
        a_a_responses = ["Adventurer: Challenges, you say? What advice do you have for a novice like me?"]
        
        a_a_a_dialogue = ["Old man: Patience, young adventurer. Explore Mottengard, learn its secrets, and forge bonds with its people. Each villager has a story, and knowledge is as valuable as any treasure. Before you rush off to Astralhaven, let the winds of fate guide you through our humble abode."]
        a_a_a_responses = ["Adventurer: Wise words, sir. Where do you recommend I begin?"]

        a_a_a_a_dialogue = ["Old man: Start with visiting the blacksmith, if you want to make it to Astralhaven you will need some good gear to get you through the dark forests."]

        text_crawl(a_dialogue[0])
        input("")
        text_crawl(a_response[0])
        input("")
        text_crawl(a_a_dialogue[0])
        input("")
        text_crawl(a_a_responses[0])
        input("")
        text_crawl(a_a_a_dialogue[0])
        input("")
        text_crawl(a_a_a_responses[0])
        input("")
        text_crawl(a_a_a_a_dialogue[0])

def mottengard_blacksmith_dialogue(dialogue_active, show_items_function, character_reference, items, show_sell_items=None):
        if dialogue_active:
            a_dialogue = ["Blacksmith: Hello how can I help you today?"]
            a_responses = ["1: I would like to purchase some equipment.", "2: Nothing goodbye."]

            a_a_dialogue = ["Blacksmith: Here browse my work."]

            exit_dialogue = ["Blacksmith: Thank you for the business sir."]

            text_crawl(a_dialogue[0])
            text_crawl(a_responses[0])
            text_crawl(a_responses[1])
            a_reply = input("Type 1 / 2\n")
            while True:
                if a_reply == "1":
                    text_crawl(add_adventurer(a_responses[0].split("1: ")[1]))
                    text_crawl(a_a_dialogue[0])
                    show_items_function()
                    while True:
                        buy_command = input("Type the name of item or exit: ")
                        all_items = list(items.keys())
                        if buy_command in all_items:
                            fetched_item = item.all_items[buy_command]
                            item_bought = character_reference.buy_items(fetched_item)
                            if item_bought:
                                text_crawl("Blacksmith: Thank you sir.")
                        elif buy_command == "exit":
                            text_crawl(exit_dialogue[0])
                            break
                        else:
                            text_crawl("Blacksmith: That item does not exist!")
                    break
                elif a_reply == "2":
                    text_crawl(add_adventurer(a_responses[1].split("2: ")[1]))
                    break
                else:
                    a_reply = input("Type 1 / 2\n")
                
mottengard_blacksmith_items = {"simple copper sword":item.simple_copper_sword, 
                                "simple copper helmet":item.simple_copper_helmet, 
                                "simple copper chestplate":item.simple_copper_chestplate}

def rookie_trainer_dialogue(dialogue_active):

    if dialogue_active:
        a_dialogue = ["Rookie trainer: To initiate combat go on interact, select the combat option and then the npc you want to enter combat with."]

        text_crawl(a_dialogue[0])

def general_store_dialogue(dialogue_active, show_items_function, character_reference, items, show_sell_items):
    if dialogue_active:
        a_dialogue = ["General store trader: Welcome, how may I help you guv?"]
        a_responses = ["1: I am looking to purchase some general goods and wares.", 
                       "2: I would like to sell some items.", 
                       "3: Sorry nothing."]

        a_a_dialogue = ["General store trader: Okay here is what I have."]

        a_b_dialogue = ["General store trader: Okay let me see what you got."]

        exit_dialogue = ["General store trader: Thank you for the business guv."]

        text_crawl(a_dialogue[0])
        text_crawl(a_responses[0])
        text_crawl(a_responses[1])
        text_crawl(a_responses[2])
        a_reply = input("Type 1 / 2 / 3\n")
        while True:
            if a_reply == "1":
                text_crawl(add_adventurer(a_responses[0].split("1: ")[1]))
                while True:
                    text_crawl(a_a_dialogue[0])
                    show_items_function()
                    buy_command = input("Type the name of item or exit: ")
                    all_items = list(items.keys())
                    if buy_command in all_items:
                        fetched_item = item.all_items[buy_command]
                        item_bought = character_reference.buy_items(fetched_item)
                        if item_bought:
                            text_crawl("General store trader: Pleasure doing business guv.")
                    elif buy_command == "exit":
                        text_crawl(exit_dialogue[0])
                        break
                    else:
                        text_crawl("General store trader: That item dun't exist!")
                break
            elif a_reply == "2":
                text_crawl(add_adventurer(a_responses[1].split("2: ")[1]))
                text_crawl(a_b_dialogue[0])
                while True:
                    character_items = list(character_reference.inventory.keys())

                    if len(character_items) == 0:
                        text_crawl("General store trader: You got nothing guv.")
                        break
                    
                    character_reference.view_inventory()
                    show_sell_items(list(character_reference.inventory.keys()))
                    sell_response = input("Type the name of the item to sell or exit: ")

                    if sell_response in list(item.all_items.keys()):
                        fetched_item = item.all_items[sell_response]
                        if fetched_item in character_items:
                            sell_value = fetched_item.value // 2
                            character_reference.gold += sell_value
                            text_crawl("General store trader: Nice doing business guv.")
                            print(f"Current gold: {character_reference.gold}")
                            character_reference.drop_item(fetched_item)
                        else:
                            text_crawl("General store trader: That dun't exist guv.")
                    elif sell_response == "exit":
                        text_crawl(exit_dialogue[0])
                        break
                    else:
                        text_crawl("General store trader: That dun't exist guv.")
                break
            elif a_reply == "3":
                text_crawl(add_adventurer(a_responses[2].split("3: ")[1]))
                break
            else:
                a_reply = input("Type 1 / 2 / 3\n")



general_store_items = {"egg":item.egg, 
                       "milk":item.milk, 
                       "flour":item.flour, 
                       "simple health potion":item.simple_health_potion, 
                       "stone axe":item.stone_axe, 
                       "basic map":item.basic_map}

inn_items = {"beer":item.beer, 
             "simple health potion":item.simple_health_potion}

def inn_trader_dialogue(dialogue_active, show_items_function, character_reference, items, show_sell_items=None):
    if dialogue_active:
        a_dialogue = ["Inn owner: Hello friend. How may I help you today?"]

        a_responses = ["1: I would like to rest and heal up.", "2: Do you have anything to sell?", "3: Nothing, just looking around."]

        a_a_dialogue = ["Inn owner: Of course, we have a room for 10 gold. How does that sound?"]

        a_a_response = ["1: Ok here is 10 gold.", "2: No thanks I'll pass."]

        a_b_dialogue = ["Inn owner: Here is what I have friend."]

        text_crawl(a_dialogue[0])
        text_crawl(a_responses[0])
        text_crawl(a_responses[1])
        text_crawl(a_responses[2])
        reply = input("Type 1 / 2 / 3\n")
        while True:
            if reply == "1":
                text_crawl(add_adventurer(a_responses[0].split("1: ")[1]))
                text_crawl(a_a_dialogue[0])
                text_crawl(a_a_response[0])
                text_crawl(a_a_response[1])
                while True:
                    rest_reply = input("Type 1 / 2\n")
                    if rest_reply == "1":
                        text_crawl(add_adventurer(a_a_response[0].split("1: ")[1]))
                        character_reference.gold -= 10

                        if character_reference.gold < 0:
                            print("Not enough gold!")
                            character_reference += 10
                            break
                        else:
                            print("You rest and are now fully healed.")
                            print(f"Current gold: {character_reference.gold}")
                            character_reference.current_health = character_reference.base_health
                            print(f"Current health: {character_reference.current_health}")
                            break
                    elif rest_reply == "2":
                        text_crawl(add_adventurer(a_a_response[1].split("2: ")[1]))
                        break
                break
            elif reply == "2":
                text_crawl(add_adventurer(a_responses[1].split("2: ")[1]))
                text_crawl(a_b_dialogue[0])
                show_items_function()
                while True:
                    buy_command = input("Type the name of item or exit: ")
                    all_items = list(items.keys())
                    if buy_command in all_items:
                        fetched_item = item.all_items[buy_command]
                        character_reference.buy_items(fetched_item)
                        text_crawl("Inn owner: Thank you friend, anything else?")
                        while True:
                            continue_response = input("Type yes/no\n")
                            if continue_response == "yes" or continue_response == "no":
                                break
                        if continue_response == "yes":
                            continue
                        elif continue_response == "no":
                            break
                    elif buy_command == "exit":
                        break
                    else:
                        text_crawl("Inn owner: I am not selling that item.")
                break
            elif reply == "3":
                text_crawl(add_adventurer(a_responses[2].split("3: ")[1]))
                break
            else:
                reply = input("Type 1 / 2 / 3\n")

                

def villager_vs_dialogue(dialogue_active):

    a_dialogue = ["Villager: If you are looking for some armour or weapons, head to the blacksmith. Otherwise head to the general store to pickup general wares and items."]

    text_crawl(a_dialogue[0])

def villager_inn_dialogue(dialogue_active):

    a_dialogue = ["Villager: I've heard whispers of a powerful tool called the Heartstone. Apparently the holder can cheat death."]
    
    text_crawl(a_dialogue[0])

def local_drunk_dialogue(dialogue_active):

    a_dialogue = ["Local drunk: You're my best friend!"]
    a_responses = ["1: I do not know you.", "2: Yes it's me."]
    text_crawl(a_dialogue[0])
    text_crawl(a_responses[0])
    text_crawl(a_responses[1])
    a_reply = input("Type 1 / 2\n")
    a_a_response = ["Local drunk: uhhhh... ok?"]
    a_b_response = ["Local drunk: Yes you are my best friend!"]

    while True:
        if a_reply == "1":
            text_crawl(add_adventurer(a_responses[0].split("1: ")[1]))
            text_crawl(a_a_response[0])
            break
        elif a_reply == "2":
            text_crawl(add_adventurer(a_responses[1].split("2: ")[1]))
            text_crawl(a_b_response[0])
            break
        else:
            print("Type 1 or 2")

def mottengard_vs_old_man_dialogue(dialogue_active):
    if dialogue_active:

        break_flag = False

        a_dialogue = ["Old man: Hello there adventurer, need something?"]

        a_responses = ["1: Yes can you remind again on how to do something.", "2: No nothing."]

        text_crawl(a_dialogue[0])
        text_crawl(a_responses[0])
        text_crawl(a_responses[1])

        a_a_dialogue = ["Old man: Of course what areas?"]

        a_a_responses = ["1: Moving.", 
                         "2: Interacting.", 
                         "3: NPCs.", 
                         "4: Inventory and equipping.", 
                         "5: Quests.", 
                         "6: Viewing stats."]
        
        a_a_a_dialogue = ["Old man: To move your character type 1 from the main menu. Then type the name of the place you want to move to."]
        a_a_b_dialogue = ["Old man: Interacting is used to interact with your environment. This includes combat, picking up items, quest interactions and leaving a main area. If you want to trade go to the npcs menu instead."]
        a_a_c_dialogue = ["Old man: If you want to start a quest, buy or sell items or talk to get information interact with NPCs. There are four types of npc: normal, trader, quest and aggresive. If you want to fight an npc, use interact menu instead."]
        a_a_d_dialogue = ["Old man: The inventory menu has two interactions, viewing and dropping items in your inventory and equipping / unequipping items. Your inventory is limited to 10 items. This can be increased however by purchasing a larger bag. You can also store items in a storage place like a bank or inn. You can also view your gold amount in your inventory."]
        a_a_e_dialogue = ["Old man: You can view your completed and incomplete quest in the quest menu. To see the next step in your quest see incompleted quests."]
        a_a_f_dialogue = ["Old man: When you view your stats you can see your combat stats, health and level experience."]

        a_a_a_a_dialogue = ["Old man: Anything else?"]

        a_a_a_a_responses = ["1: Yes.", "2: No."]

        reply = input("Type 1 / 2\n")
        while True:
            if reply == "1":
                text_crawl(add_adventurer(a_responses[0].split("1: ")[1]))
                while break_flag == False:
                    text_crawl(a_a_dialogue[0])
                    for text in a_a_responses:
                        text_crawl(text)
                    second_reply = input("Type the number\n")
                    if second_reply == "1":
                        text_crawl(add_adventurer(a_a_responses[0].split("1: ")[1]))
                        text_crawl(a_a_a_dialogue[0])
                    elif second_reply == "2":
                        text_crawl(add_adventurer(a_a_responses[1].split("2: ")[1]))
                        text_crawl(a_a_b_dialogue[0])
                    elif second_reply == "3":
                        text_crawl(add_adventurer(a_a_responses[2].split("3: ")[1]))
                        text_crawl(a_a_c_dialogue[0])
                    elif second_reply == "4":
                        text_crawl(add_adventurer(a_a_responses[3].split("4: ")[1]))
                        text_crawl(a_a_d_dialogue[0])
                    elif second_reply == "5":
                        text_crawl(add_adventurer(a_a_responses[4].split("5: ")[1]))
                        text_crawl(a_a_e_dialogue[0])
                    elif second_reply == "6":
                        text_crawl(add_adventurer(a_a_responses[5].split("6: ")[1]))
                        text_crawl(a_a_f_dialogue[0])                
                    else:
                        print("Type a valid number.")

                    text_crawl(a_a_a_a_dialogue[0])
                    text_crawl(a_a_a_a_responses[0])
                    text_crawl(a_a_a_a_responses[1])
                    exit_reply = input("Type 1 / 2\n")
                    while True:
                        if exit_reply == "1":
                            text_crawl(add_adventurer(a_a_a_a_responses[0].split("1: ")[1]))
                            break
                        elif exit_reply == "2":
                            text_crawl(add_adventurer(a_a_a_a_responses[1].split("2: ")[1]))
                            break_flag = True
                            break
                        else:
                            print("Type 1 / 2\n")
                break
            elif reply == "2":
                text_crawl(add_adventurer(a_responses[1].split("2: ")[1]))
                break
            else:
                print("Type 1/2")

def mottengard_guard_dialogue(dialogue_active):
    if dialogue_active:
        a_dialogue = ["Guard: If you follow that path it leads to the Mythos Forests. Make sure you are well prepared with plenty of resources and gear."]

        text_crawl(a_dialogue[0])

def inn_chef_dialogue(dialogue_active, quest_reference):
    if dialogue_active:

        if quest_reference.activate_quest == False and quest_reference.step_one_flag == False and quest_reference.step_two_flag == False and quest_reference.complete == False:
            a_dialogue = ["Inn chef: Hello, how may I help you?"]

            a_response_original = ["Adventurer: I am looking for work."]

            a_a_dialogue = ["Inn chef: Great I am preparing a banquet for guests later. I am running low on some ingredients. Bring me 2 eggs, 1 milk and 1 flour."]

            text_crawl(a_dialogue[0])
            text_crawl(a_response_original[0])
            text_crawl(a_a_dialogue[0])

        elif quest_reference.step_one_flag == True or quest_reference.step_two_flag == True:
            a_dialogue_quest_started = ["Inn chef: I need 2 eggs, 1 milk and 1 flour."]

            text_crawl(a_dialogue_quest_started[0])

        if quest_reference.complete == True:
            a_dialogue_quest_completed = ["Inn chef: Thanks again for your help, would not have been able to complete that cake in time without your help."]

            text_crawl(a_dialogue_quest_completed[0])
common_exp_ranges = {1:(1,3), 
                     2:(3,6), 
                     3:(5,8), 
                     4:(7,10), 
                     5:(10,15), 
                     6:(15,25), 
                     7:(25, 40), 
                     8:(40, 80), 
                     9:(80, 120), 
                     10:(120, 250), 
                     11:(250, 500), 
                     12:(500, 800), 
                     13:(800, 1500),
                     14:(1300, 2000), 
                     15:(2000, 3000), 
                     16:(3000, 5000), 
                     17:(4500, 8000), 
                     18:(8000, 13000), 
                     19:(13000, 19000), 
                     20:(18000, 22000), 
                     21:(22000, 25000), 
                     22:(23000, 27000), 
                     23:(25000, 30000)}

boss_exp_ranges = "custom values"


mottengard_old_man = Npc(health=1, base_health=1, attack=0, defence=0, npc_type="normal", dialogue=mottengard_vs_old_man_dialogue)
mottengard_guard = Npc(health=1, base_health=1, attack=0, defence=0, npc_type="normal", dialogue=mottengard_guard_dialogue)
villager_vs = Npc(health=1, base_health=1, attack=0, defence=0, npc_type="normal", dialogue=villager_vs_dialogue)
villager_inn = Npc(health=1, base_health=1, attack=0, defence=0, npc_type="normal", dialogue=villager_inn_dialogue)
local_drunk = Npc(health=1, base_health=1, attack=0, defence=0, npc_type="normal", dialogue=local_drunk_dialogue)
inn_trader = Trader(health=1, base_health=1, attack=0, defence=0, npc_type="trader", dialogue=inn_trader_dialogue, items=inn_items)
general_store_trader = Trader(health=1, base_health=1, attack=0, defence=0, npc_type="trader", dialogue=general_store_dialogue, items=general_store_items)
mottengard_blacksmith = Trader(health=1, base_health=1, attack=0, defence=0, npc_type="trader", dialogue=mottengard_blacksmith_dialogue, items=mottengard_blacksmith_items)
rookie_trainer = Aggresive(health=8, base_health=8, attack=2, defence=0, npc_type="aggressive", dialogue=rookie_trainer_dialogue, skill_level=1, common_exp_ranges=common_exp_ranges)
inn_chef = Quest(health=1, base_health=1, attack=0, defence=0, npc_type="quest", dialogue=inn_chef_dialogue, quest_reference="Cake Quest")
mottengard_tutorial_old_man = Quest(health=1, base_health=1, attack=0, defence=0, npc_type="quest", dialogue=mottengard_old_man_dialogue, quest_reference="Tutorial Quest")

mottengard_npcs = {"old man":mottengard_old_man, 
                   "blacksmith":mottengard_blacksmith, 
                   "rookie trainer":rookie_trainer, 
                   "general store trader":general_store_trader, 
                   "villager vs":villager_vs, 
                   "villager inn":villager_inn, 
                   "local drunk":local_drunk, 
                   "guard":mottengard_guard, 
                   "tutorial man":mottengard_tutorial_old_man, 
                   "inn trader":inn_trader, 
                   "inn chef":inn_chef}


if __name__ == "__main__":
    from character import PlayerCharacter
    from quest import quest_database
    import world
    import item
    from random import randint

    test_character = PlayerCharacter(base_health=15, base_attack=1, base_defence=0, level=1, current_map=world.Mottengard(), quest_database=quest_database)
    test_character.pickup_item(item.all_items["simple health potion"])
    test_character.pickup_item(item.all_items["simple health potion"])
    test_character.view_inventory()
    enemy_npc = rookie_trainer

    while True:
        print(f"Your health: {test_character.current_health}, Enemy Remaining health: {enemy_npc.health}")
        combat_response = input("Select options: attack / item / run\n")
        if combat_response == "attack":
            damage_inflicted = test_character.attack_target(enemy_npc)
            print(f"You attack and deal {damage_inflicted} damage.")
            if enemy_npc.health <= 0:
                print("You have won the battle!")
                break
            damage_taken = test_character.defend_target(enemy_npc)
            print(f"The enemy deals {damage_taken} damage.")
            if test_character.current_health <= 0:
                print("You have died!")
        elif combat_response == "item":
            while True:
                test_character.view_inventory()
                item_response = input("Type item name / exit\n")

                if item_response == "exit":
                    break

                if item_response not in list(item.all_items.keys()):
                    print("Invalid item.")
                else:
                    test_character.use_item(item.all_items[item_response])
        elif combat_response == "run":
            random_number = randint(1,3)
            if random_number == 1:
                print("Succesfully escape!")
                break
            else:
                print("Failed to escape.")
        else:
            print("Invalid command.")

    print(test_character.defeated_npcs)

