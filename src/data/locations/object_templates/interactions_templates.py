from random import randint

class Interactions:

    def __init__(self, logic_input, player_reference):
        self.logic_input = logic_input
        self.player_reference = player_reference

    def run_logic(self, **kwargs):
        self.logic_input(kwargs)

class Quest(Interactions):

    def __init__(self, logic_input, player_reference, quest_reference):
        super().__init__(logic_input, player_reference)

        self.interaction_type = "quest"
        self.activated = False
        self.quest_reference = quest_reference

    def run_logic(self, **kwargs):
        self.logic_input(kwargs)
        self.interaction_activated()
        
    def interaction_activated(self):
        if self.quest_reference.quest_active:
            self.activated = True


class Combat():

    def __init__(self, player_reference, local_npc_database, npc_conds):

        self.player_reference = player_reference
        self.interaction_type = "combat"
        self.available_aggressive_npcs = []
        self.local_npc_database = local_npc_database
        self.npc_conds = npc_conds

    # ---------- Pre combat menu ---------- #

    # To be done
    def update_combat_npcs(self):
        """Update the status of combat npcs. First filter for combat npcs.
        Run availability conditions to make npc available or unavailable.
        Finally append available npcs and remove unavailable npcs.

        self.npc_conds format: {npc_object: npc_condition}
        
        Args:
            To be done in future
            cond_type: Either on or off. If on will check for on conditions
            to make npc availble, otherwise for off conditions to make npc
            unavailable."""

        # Check local npc database for combat npcs.
        combat_npcs = [npc for npc in self.local_npc_database.values() if npc.npc_type == "combat"]

        # # Make npcs available or unavailable. 
        # # Certain combat NPCs if defeated cannot enter combat again
        # # For example Quest combat NPCs.
        # if cond_type == "on":
        #     # Check the condition to make npc available. 
        #     # If condition satisfied make it available.
        #     for npc, condition in self.npcs_conds.items():
        #         npc.check_on_condition(condition)
        # elif cond_type == "off":
        #     # Check the condition to make npc unavailable.
        #     # If condition satisfied make it unavailable.
        #     for npc, condition in self.npcs_conds.items():
        #         npc.check_off_condition(condition)

        # Collect available aggressive npcs and remove unavailable aggressive npcs.
        for npc in combat_npcs:
            if npc.available == True and npc not in self.available_aggressive_npcs:
                self.available_aggressive_npcs.append(npc)
            
            if npc.available == False and npc in self.available_aggressive_npcs:
                self.available_aggressive_npcs.remove(npc)

    def gather_combat_npcs(self):
        """Create a list of the names of available aggressive npcs.
        
        Args:
            None

        Returns:
            None"""

        self.avail_combat_npcs = {str(i + 1): npc.name for i, npc in enumerate(self.available_aggressive_npcs)}

    def show_pre_combat_menu(self):
        """Show pre combat menu.
        
        Args:
            None
            
        Returns:
            None"""
        combat_npc_list = ""

        for i, npc in self.avail_combat_npcs.items():
            combat_npc_list += f" -- {i}: {npc}"

        combat_npc_list += " --"

        print("Available Combat NPCs:")
        print(combat_npc_list)
        
    def fetch_npc_response(self):
        """Fetch the player response for npc to enter
        combat.
        
        Args:
            None
            
        Returns:
            The chosen npc to fight."""

        npc_response = input("Type number of npc or 0 to exit: ")
        return npc_response    

    def run_pre_combat(self):
        """Run the pre combat menu and gather available combat npcs.
        
        Args:
            None
            
        Returns:
            Chosen NPC to fight."""
        self.update_combat_npcs()
        self.gather_combat_npcs()

        while True:
            self.show_pre_combat_menu()
            npc_response = self.fetch_npc_response()

            if npc_response == "0":
                return npc_response
            elif npc_response not in self.avail_combat_npcs:
                print("Invalid npc inputted.")
            else:
                return npc_response

    # ---------- Main combat sequence ---------- #

    def show_combat_menu(self, npc):
        """Show combat menu with npc and player health stats.
        
        Args:
            npc: The npc object to show on the menu."""
        stats = f" Player health: {self.player_reference.current_health} / {self.player_reference.base_health}       NPC health: {npc.current_health} / {npc.base_health}"
        options = " -- 1 Attack -- 2 Use Item -- 3 Run --"
        
        print(stats)
        print(options)

    # ---------- Combat responses ---------- #

    def attack_response(self, npc):
        """Run the attack response.
        
        Args:
            npc: The npc object to run the combat sequence
            with."""
        battle_outcome = npc.run_combat_sequence(self.player_reference)
        return battle_outcome

    def use_item_response(self):
        """Run the use item response"""
        self.player_reference.run_use_item_menu()

    def run_response(self):
        """Run the escape response"""
        random_number = randint(1, 3)

        if random_number == 1:
            print("Successfully escaped!")
            return True
        else:
            print("Failed to escape")
            return False

    def enter_combat(self, npc):
        """Enter combat method with different combat responses.
        
        Args:
            npc: The npc object to enter combat with."""
        potential_responses = ["1", "2", "3"]
        self.player_reference.in_combat = True
        print(f"Combat started with {npc.name}")
        
        while self.player_reference.in_combat:
            self.show_combat_menu(npc)
            combat_response = input("Select response: ")

            if combat_response not in potential_responses:
                print("Invalid response, type 1, 2 or 3.")
                continue

            if combat_response == "1":
                battle_outcome = self.attack_response(npc)
                if battle_outcome:
                    break
            elif combat_response == "2":
                self.use_item_response()
            elif combat_response == "3":
                run_outcome = self.run_response()
                if run_outcome:
                    break
            
    # ---------- Master function ---------- #

    def run_combat(self):
        """Run combat interaction logic.
        
        Args:
            """
        selected_npc_response = self.run_pre_combat()
        
        npcs = {npc.name: npc for npc in self.available_aggressive_npcs}

        npc_name = self.avail_combat_npcs[selected_npc_response]

        if selected_npc_response != "0":
            selected_npc = npcs[npc_name]
            self.enter_combat(selected_npc)

    def run_logic(self):
        """Run logic. Kwargs will be npc_conds."""
        self.run_combat()
