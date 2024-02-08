import npc
import item

class Quest:

    def __init__(self):
        self.requirements = ""
        self.rewards = ""
        self.complete = False
        self.step_one_complete = False

    def step_one(self):
        
        # Details listed in journal
        goal = ""

        # Quest condition



class TutorialQuest(Quest):

    def __init__(self):
        self.quest_name = "Tutorial Quest"
        self.requirements = "Talk to the old man"
        self.rewards = "10 exp, 2 x Apple"
        self.character = None

        self.quest_active = False

        self.activate_quest = False
        self.complete = False

        # Flags
        self.step_one_flag = False
        self.step_two_flag = False
        self.step_three_flag = False

        # Current goal
        self.current_goal = ""

    def step_one(self):
        
        # Details listed in journal
        self.current_goal = "Buy a simple copper sword from the blacksmith."
    
        if item.all_items["simple copper sword"] in list(self.character.inventory.keys()):
            print("Step one complete!")
            self.step_one_flag = False
            self.step_two_flag = True

    def step_two(self):

        # Details listed in journal
        self.current_goal = "Equip the sword."

        if item.all_items["simple copper sword"] == self.character.equipped_weapon:
            print("Step two complete!")
            self.step_two_flag = False
            self.step_three_flag = True

    def step_three(self):

        self.current_goal = "Defeat the trainer at the training grounds."

        if npc.mottengard_npcs["rookie trainer"] in self.character.defeated_npcs.keys():
            print("Quest complete! Gained 10 exp and 2 apples.")
            
            self.character.gain_exp(10)
            self.character.pickup_item(item.all_items["apple"])
            self.character.pickup_item(item.all_items["apple"])

            self.quest_active = False
            self.step_three_flag = False
            self.complete = True

    def run_quest(self):

        if self.complete == False:
            # Initial run
            if self.step_one_flag == False and self.activate_quest == True:
                print(f"{self.quest_name} started.")
                self.quest_active = True
                self.step_one_flag = True
                self.activate_quest = False
            
            if self.step_one_flag:
                self.step_one()

            if self.step_two_flag:
                self.step_two()

            if self.step_three_flag:
                self.step_three()

class MottengardInnCookingQuest(Quest):

    def __init__(self):
        self.quest_name = "Cake Quest"
        self.requirements = "Talk to the inn chef."
        self.rewards = "10 exp, 35 gold, 1 x cake"
        self.character = None

        self.quest_active = False

        self.activate_quest = False
        self.complete = False

        # Flags
        self.step_one_flag = False

        self.step_one_flour_flag = False
        self.step_one_milk_flag = False
        self.step_one_egg_flag = False

        self.step_two_flag = False

        # Current goal
        self.current_goal = ""

    def step_one(self):
        
        # Details listed in journal
        self.current_goal = "Buy 2 eggs, 1 flour and 1 milk."
    
        if item.all_items["flour"] in list(self.character.inventory.keys()):
            self.step_one_flour_flag = True
        
        if item.all_items["milk"] in list(self.character.inventory.keys()):
            self.step_one_milk_flag = True

        if item.all_items["egg"] in list(self.character.inventory.keys()) and self.character.inventory[item.all_items["egg"]] == 2:
            self.step_one_egg_flag = True
            
        if self.step_one_flour_flag == True and self.step_one_milk_flag == True and self.step_one_egg_flag == True:
            print("Step one complete!")
            self.step_one_flag = False
            self.step_two_flag = True

    def step_two(self):

        self.current_goal = "Give the ingredients to the chef."

        if self.character.active_dialogue_npc == npc.mottengard_npcs["inn chef"]:
            print("Quest complete! Gained 10 exp, 35 gold and cake.")
            
            self.character.gain_exp(10)
            self.character.gold += 35
            self.character.pickup_item(item.all_items["cake"])

            self.quest_active = False
            self.step_two_flag = False
            self.complete = True

    def run_quest(self):

        if self.complete == False:
            # Initial run
            if self.step_one_flag == False and self.activate_quest == True:
                print(f"{self.quest_name} started.")
                self.quest_active = True
                self.step_one_flag = True
                self.activate_quest = False
            
            if self.step_one_flag:
                self.step_one()

            if self.step_two_flag:
                self.step_two()


quest_database = {"Tutorial Quest":TutorialQuest(), "Cake Quest":MottengardInnCookingQuest()}

