class Quest:

    def __init__(self, 
                 quest_name, 
                 requirements_desc, 
                 rewards, 
                 rewards_description,
                 activation_condition, 
                 maximum_steps, 
                 all_goals, 
                 all_conditions):
        """Class attributes:
        
        Input Attributes:
            quest_name: Name of the quest. Input must be string datatype.
            requirements_desc: Description on how to begin the quest. Must be string datatype.
            rewards: A dictionary of the rewards and the number of reward items.
            rewards_description: A description of the rewards. Must be a string datatype.
            activation_condition: An input function which returns true if the activation
            condition is satisfied.
            maximum_steps: The number of steps needed required for completion of the quest.
            all_goals: A dictionary of all descriptions of the conditions for each step of the quest.
            Dictionary follows a format of {step_number:"Condition description"}. The final step
            of the dictionary states the completion description.

            Completion description - "Brief description of how quest achieved, rewards gained."

            all_conditions: A dictionary of the condition functions for each step of the quest.
            Dictionary follows a format of {step_number:condition_function}.
            
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

    def activate_quest(self):
        """If the activation condition is satisfied, return true from
        the activation condition function, setting the quest to active.
        Initialise the conditions and goals (condition description)."""
        if self.activation_condition == True and self.complete == False and self.quest_active == False:
            self.quest_active = True
            self.update_conditions()

    def check_quest(self, player_reference):
        """Checks if quest conditions have been achieved to move on next step.
        If final step completed, set quest to complete and give rewards."""

        if self.current_condition == True and self.quest_active == True:
            self.progress_step()
            self.update_conditions()

        if self.current_step > self.maximum_steps:
            self.set_quest_complete()
            self.set_status_complete(player_reference=player_reference)
            self.give_reward(player_reference=player_reference)

    def set_status_complete(self, player_reference):
        """Move the quest from ongoing status to completed status. 
        
        Args:
            player_reference: To access the player quest data."""
        
        del player_reference.ongoing_quest_list[self.quest_name]
        player_reference.completed_quest_list[self.quest_name] = self.current_goal

    def set_quest_complete(self):
        """If quest completion objective achieved, set quest to inactive
        and complete."""
        self.quest_active = False
        self.complete = True

    def give_reward(self, player_reference):
        """Give reward to the player. 
        Args:
            player_reference: Player reference to enable pickup method."""
        
        for reward, quantity in self.rewards.items():
            for _ in range(1, quantity + 1):
                player_reference.pickup(reward)
        
        print(f"Acquired {self.rewards_description}")

    def progress_step(self):
        """Move the quest forward onto next step."""
        self.current_step += 1

    def update_conditions(self):
        """Updates the step condition and condition description."""
        self.current_goal = self.all_goals[self.current_step]
        self.current_condtion = self.all_conditions[self.current_step]


        





        