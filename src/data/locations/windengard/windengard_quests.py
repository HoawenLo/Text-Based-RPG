from ..object_templates.quests_templates import *

class WindengardQuests:

    def __init__(self, rewards, item_database, npc_database, player_reference):
        """Format of rewards input:
        
        rewards: {"exp":amount, "gold":amount, "item_name":(item_number, items)}"""

        self.item_database = item_database
        self.npc_database = npc_database
        self.player_reference = player_reference
        
        # --------------- Quest condtions --------------- #

        def tutorial_quest_conditions(cond_type):
            """All conditions for the tutorial quest.
            
            Args:
                cond_type: Either activation or quest_steps.
                
            Returns:
                The relevant condition as a function."""
            
            def set_active():
                """No activation condition check needed, instead set 
                to active after old man dialogue finished."""

                # The end of the Old man dialogue.

                return True
            
            def step_one():
                """Step one: Purchase simple copper sword from the blacksmith."""

                if self.item_database["Simple copper sword"] in list(self.player_reference.inventory.keys()):
                    return True
                else:
                    return False
                
            def step_two():
                """Step two: Equip the simple copper sword."""

                if self.player_reference.equipped_weapon == self.item_database["Simple copper sword"]:
                    return True
                else:
                    return False
                
            def step_three():
                """Step three: Defeat the rookie trainer at the training ground."""

                if self.npc_database["rookie_trainer"] in list(self.player_reference.defeated_npcs.keys()):
                    return True
                else:
                    return False

            conditions = {1:step_one, 2:step_two, 3:step_three}


            if cond_type == "set_active":
                return set_active
            if cond_type == "conditions":
                return conditions

        # --------------- All goals --------------- #

        tutorial_quest_goals = {1:"Purchase simple copper sword from the blacksmith.",
                                2:"Equip the simple copper sword.",
                                3:"Defeat the rookie trainer at the training ground."}
        
        # --------------- All quests --------------- #

        self.tutorial_quest = Quest(quest_name="Tutorial quest", 
                                    requirements_desc="Initiate upon starting the game.", 
                                    rewards=rewards["tutorial_quest"], 
                                    rewards_description="Completed the tutorial quest and gained 20 exp, 50 gold and 2 x Apples", 
                                    activation_condition=tutorial_quest_conditions(cond_type="set_active"),
                                    maximum_steps=3,
                                    all_goals=tutorial_quest_goals, 
                                    all_conditions=tutorial_quest_conditions(cond_type="conditions"), 
                                    player_reference=player_reference,
                                    quest_npc=npc_database["oldman_intro"])
