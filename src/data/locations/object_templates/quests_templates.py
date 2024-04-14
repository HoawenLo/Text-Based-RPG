class Quest:

    def __init__(self, 
                 quest_name, 
                 requirements_desc, 
                 rewards, 
                 rewards_description,
                 activation_condition, 
                 maximum_steps, 
                 all_goals, 
                 all_conditions, 
                 player_reference,
                 quest_npc):
        """Class attributes:
        
        Input Attributes:
            quest_name: Name of the quest. Input must be string datatype.
            requirements_desc: Description on how to begin the quest. Must be string datatype.
            rewards: A dictionary of the rewards and the number of reward items.
            rewards_description: A description of the rewards. Must be a string datatype.
            activation_condition: An input function which returns true if the activation
            condition is satisfied.
            maximum_steps: The number of steps needed required for completion of the quest.
            all_goals: A list of all descriptions of the conditions for each step of the quest.
            Dictionary follows a format of {step_number:"Condition description"}. The final step
            of the dictionary states the completion description.

            Completion description - "Brief description of how quest achieved, rewards gained."

            all_conditions: A dictionary of the condition functions for each step of the quest.
            Dictionary follows a format of {step_number:condition_function}.
            player_reference: The player reference.
            quest_npc: The quest npc linked to the quest.
        
        Format of rewards input:
        
        rewards: {"exp":amount, "gold":amount, "item_name":(item_number, items)}

        Non Input Attributes:
            quest_active: Boolean which states if quest active or not. Prevents quest
            from activating from the start.
            complete: Boolean which states if quest complete or not. Prevents quest from
            activating again if complete."""
        
        # Quest overview
        self.quest_name = quest_name
        self.requirements_desc = requirements_desc

        # Quest control booleans
        self.quest_active = False
        self.complete = False

        # Rewards
        self.rewards = rewards
        self.rewards_description = rewards_description

        # Quest activation condition
        self.activation_condition = activation_condition
        
        # Quest step controls, descriptions and conditions
        self.current_step = 1
        self.maximum_steps = maximum_steps

        self.all_goals = all_goals
        self.current_goal = ""
        
        self.all_conditions = all_conditions
        self.current_condition = None

        # Player reference
        self.player_reference = player_reference

        # Quest npc
        self.quest_npc = quest_npc

        # Feed quest into quest npc
        self.quest_npc.quest_reference = self

    def activate_quest(self):
        """If the activation condition is satisfied, return true from
        the activation condition function, setting the quest to active.
        Initialise the conditions and goals (condition description)."""

        if self.activation_condition() == True and self.complete == False and self.quest_active == False:
            self.quest_active = True
            self.initialise_conditions()
            self.player_reference.add_quest(self)
            

    def check_quest(self):
        """Checks if quest conditions have been achieved to move on next step.
        If final step completed, set quest to complete and give rewards."""

        if self.current_condition() == True and self.quest_active == True:
            self.progress_step()

        if self.current_step > self.maximum_steps:
            self.set_quest_complete()
            self.set_status_complete()
            print(f"Quest update: {self.quest_name} complete!")
            self.give_reward()
        
        # Placed here as want to not update conditions if self.current_step
        # > self.maximum_steps meaning that all steps have been completed.
        # The self.set_status_complete will set self.quest_active to False
        # hence will not attempt to update_conditions. If attempt to update
        # conditions will get KeyError (no more steps to update to).
        if self.current_condition() == True and self.quest_active == True:
            self.update_conditions()



    def set_status_complete(self):
        """Move the quest from ongoing status to completed status. 
        
        Args:
            None
            
        Returns:
            None"""
        
        del self.player_reference.ongoing_quest_list[self.quest_name]
        self.player_reference.completed_quest_list[self.quest_name] = self.rewards_description

    def set_quest_complete(self):
        """If quest completion objective achieved, set quest to inactive
        and complete."""
        self.quest_active = False
        self.complete = True

    def give_reward(self):
        """Give reward to the player. 
        Args:
            None
            
        Returns:
            None"""
        
        for reward_type, reward in self.rewards.items():
            
            if reward_type == "exp":
                self.player_reference.gain_exp(reward)
                continue
            elif reward_type == "gold":
                self.player_reference.gold += reward
                continue
            
            item = reward[0]
            quantity = reward[1]

            for _ in range(1, quantity + 1):
                self.player_reference.pickup_item(item)
        
        print(f"Acquired {self.rewards_description}")

    def progress_step(self):
        """Move the quest forward onto next step."""
        self.current_step += 1

    def initialise_conditions(self):
        """Initialise quest conditions."""
        
        self.current_goal = self.all_goals[self.current_step]
        self.current_condition = self.all_conditions[self.current_step]
        print(f"Quest update: {self.quest_name} started.")
        print(f"Quest update: {self.quest_name}, New goal, {self.current_goal}")


    def update_conditions(self):
        """Updates the step condition and condition description."""

        print(f"Quest update:  {self.quest_name}, Step {self.current_step} achieved.")
        self.current_goal = self.all_goals[self.current_step]
        self.current_condition = self.all_conditions[self.current_step]
        print(f"Quest update: {self.quest_name}, New goal, {self.current_goal}")



        


        





        