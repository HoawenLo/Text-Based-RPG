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


class Combat(Interactions):

    def __init__(self, player_reference):
        super().__init__(player_reference)

        self.interaction_type = "combat"
        self.available_aggressive_npcs = []

    # ---------- Pre combat menu ---------- #

    def update_combat_npcs(self, area_data_npcs, cond_type, npcs_conds):
        """Update the status of combat npcs. First filter for combat npcs.
        Run availability conditions to make npc available or unavailable.
        Finally append available npcs and remove unavailable npcs.
        
        Args:
            area_data_npcs: The npcs of the area the player is in.
            cond_type: Either on or off. If on will check for on conditions
            to make npc availble, otherwise for off conditions to make npc
            unavailable.
            npc_conds: The supplied npc condtions with the linked npc. Is
            a dictionary of format {npc_object: npc_condition}"""

        # break into function
        combat_npcs = [i for i in area_data_npcs if i.npc_type == "combat"]

        if cond_type == "on":
            for npc, condition in npcs_conds.items():
                npc.check_on_condition(condition)
        elif cond_type == "off":
            for npc, condition in npcs_conds.items():
                npc.check_off_condition(condition)

        # Break into function
        for npc in combat_npcs:
            if npc.available == True and npc not in self.available_aggressive_npcs:
                self.available_aggressive_npcs.append(npc)
            
            if npc.available == False and npc in self.available_aggressive_npcs:
                self.available_aggressive_npcs.remove(npc)

    def gather_combat_npcs(self):
        """List available combat npcs in name format."""

        avail_combat_npcs = [npc.name for npc in self.available_aggressive_npcs]

        return avail_combat_npcs

    def show_pre_combat_menu(self, available_npcs):
        """Show pre combat menu.
        
        Args:
            available_npcs: The available combat npcs."""

        combat_npc_list = ""

        for npc in available_npcs:
            combat_npc_list += f" -- {npc}"

        combat_npc_list += " --"

        print("Available Combat Npcs:")
        print(combat_npc_list)
        
    def fetch_npc_response(self):
        """Fetch the player response for npc to enter
        combat."""

        npc_response = input("Type name of npc or exit: ")
        return npc_response    

    def run_pre_combat(self, available_npcs):
        """Run the pre combat menu and gather available combat npcs.
        
        Args:
            available_npcs: The available npcs to enter combat with.
            Is a list with npc.name values."""
        
        self.update_combat_npcs()
        available_npcs = self.gather_combat_npcs()

        while True:
            self.show_pre_combat_menu(available_npcs)
            npc_response = self.fetch_npc_response()

            if npc_response == "exit":
                break
            elif npc_response not in available_npcs:
                print("Invalid npc inputted.")
            else:
                return npc_response

    # ---------- Main combat sequence ---------- #

    def show_combat_menu(self, npc):
        """Show combat menu with npc and player health stats.
        
        Args:
            npc: The npc object to show on the menu."""
        stats = f" {self.player_reference.current_health} / {self.player_reference.base_health}       {npc.current_health} / {npc.base_health}"
        options = " -- 1 Attack -- 2 Use Item -- 3 Run --"
        
        print(stats)
        print(options)

    # ---------- Combat responses ---------- #

    def attack_response(self, npc):
        """Run the attack response.
        
        Args:
            npc: The npc object to run the combat sequence
            with."""
        npc.run_combat_sequence(self.player_reference)

    def use_item_response(self):
        """Run the use item response"""
        self.player_reference.run_use_item_menu()

    def run_response(self):
        """Run the escape response"""
        random_number = randint(1, 3)

        if random_number == 1:
            print("Successfully escaped!")
        else:
            print("Failed to escape")

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
                self.attack_response(npc)
            elif combat_response == "2":
                self.use_item_response()
            elif combat_response == "3":
                self.run_response()
            
    # ---------- Master function ---------- #

    def run_combat(self, area_data_npcs):
        """Run combat interaction logic.
        
        Args:
            area_data_npcs: The npcs available in this area.
            Needed to get the available combat npcs."""

        selected_npc_response = self.run_pre_combat()
        
        if selected_npc_response != "exit":
            selected_npc = area_data_npcs[selected_npc]
            self.enter_combat(selected_npc)

    def run_logic(self, **kwargs):
        """Run logic. Kwargs will be area_data_npcs."""
        self.run_combat(kwargs)
