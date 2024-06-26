import dill
import os

from .text_manipulation.text_manipulation import *
from .data.game_data import GameData


# Connects the data to the player and handles input.

class Engine:

    def __init__(self):

        # ----------------------- Intialisation variables ----------------------- #


        # ----------------------- Title and loading text ----------------------- #

        self.title_screen = "Chronicles of Eldoria"

        script_directory = os.path.dirname(os.path.abspath(__file__))
        text_file_path = "data/text_data/load_new_game.txt"
        file_path = os.path.join(script_directory, text_file_path)

        with open(file_path, "r") as file:
            self.title_intro_txt = file.read()

        # ----------------------- Game state ----------------------- #

        self.game_running = False

        # ----------------------- Main Menu ----------------------- #

        self.main_menu_responses = ["1", "2", "3"]

        # ----------------------- Player Menu ----------------------- #

        self.player_menu_responses = ["1", "2", "3", "4", "5", "6"]
        self.player_menu_table = {"1":self.move_response, 
                                  "2":self.inventory_response, 
                                  "3":self.interactions_response, 
                                  "4":self.quests_response, 
                                  "5":self.stats_response, 
                                  "6":self.save_exit_response}

        self.player_menu_options = ["1 Move", 
                                    "2 Inventory", 
                                    "3 Interact", 
                                    "4 Quests", 
                                    "5 Stats", 
                                    "6 Save and Exit"]

        # ----------------------- Quest Menu ----------------------- #

        self.quest_menu_responses = ["1", "2", "3"]

        # ----------------------- Inventory Menu ----------------------- #

        self.inventory_menu_responses = ["1", "2", "3"]

        # ----------------------- In Game Menu ----------------------- #

        

    # ------------------------------------- Master -------------------------------------
        
    def run_engine(self):
        """Runs the game engine."""

        while True:
            print("Select option (type number) -- 1 Play -- 2 Lore -- 3 Exit -- ")
            response = input("Response: ")

            if response not in self.main_menu_responses:
                print("Type 1, 2 or 3.")
            
            if response == "1":
                self.play()
            elif response == "2":
                print("Under development.")
            elif response == "3":
                break    

    def load_title_screen(self):
        """Loads the title screen."""

        character_crawl(self.title_screen, text_speed=0.3)
        character_crawl(self.title_screen, text_speed=0.01)
        print(self.title_screen)

    def load_intro_text(self):
        """Loads the prologue text."""

        word_crawl(self.title_intro_txt, text_speed=0.1, line_length=60)
        input("Press any key to continue ")

    def set_player_settings(self):
        """Initialise the new start state for the player."""

        initial_state = GameData(None).game_data

        player = initial_state["player"]

        self.player = player(base_health=15, 
                             base_attack=1, 
                             base_defence=0, 
                             level=1, 
                             current_location=None)

        # Initialise game_data
        
        self.game_data = GameData(self.player).game_data

        self.player.current_area = "Caravan"
        self.player.current_location = self.game_data["locations"]["windengard"]
        self.player.area_data = self.player.current_location[self.player.current_area]


        # Activate tutorial
        self.game_data["intro_quest"].windengard_reference.npcs["oldman_intro"].run_dialogue(dialogue_active=True)


    
    # ------------------------------------- Game state -------------------------------------

    def play(self):
        """Run the play option."""
        
        if os.path.isfile("saved_states/savegame.pkl"):

            print("Save file detected.")

            while True:
                print("Start a new game? 1 Yes / 2 No")
                response = self.fetch_response()
                
                if response == "1" or response == "2":
                    break
                else:
                    print("Invalid response. Type 1 or 2.")
                
            if response == "1":
                self.game_running = True
                self.load_new_game()
                self.run_game()
            elif response == "2":
                self.player = self.load_saved_game("saved_states/savegame.pkl")
                self.game_data = GameData(self.player).game_data
                self.game_running = True
                self.run_game()
        else:
            self.load_new_game()
            self.game_running = True
            self.run_game()

    def load_new_game(self):
        """Load a new game."""

        self.load_title_screen()
        self.load_intro_text()
        self.set_player_settings()

    def run_game(self):
        while self.game_running:
            self.show_ingame_menu()
            self.handle_input()
            self.check_quests()

    def save_game(self, filename):
        """"Save game with pickle."""

        with open(filename, "wb") as file:
            dill.dump(self.player, file)
        print("Game saved!")

    def load_saved_game(self, filename):
        """Load a save pickle file."""

        with open(filename, "rb") as file:
            loaded_game = dill.load(file)
        return loaded_game

    # ------------------------------------- In game events cycle -------------------------------------

    

    # add inventory storage value
    def show_ingame_menu(self, line_length=71):
        """Shows the player menu.
        
        Args:
            line_length: The maximum line length of the player menu.
            Default is 51.
            available_interactions: The available interactions of the place."""
        
        line = "-" * line_length

        available_interactions = list(self.player.area_data["interactions"])
        available_interactions = self.fill_interaction_gaps(available_interactions)

        equipped_items = self.return_equipped_names()
        
        print(line)
        print(f"Health: {self.player.current_health} / {self.player.base_health}    Current Area: {self.player.current_area}    Gold: {self.player.gold}    Inventory space: {self.player.inventory_size} / {self.player.max_inventory_size}")
        print(line)
        print(combine_characters(f"Helmet {equipped_items[0]}", f"Weapon: {equipped_items[2]}", line_length=51))
        print(combine_characters(f"Chestplate: {equipped_items[1]}", f"Ring: {equipped_items[3]}", line_length=51))
        print(line)
        for i in range(len(self.player_menu_options)):
            print(combine_characters(self.player_menu_options[i], available_interactions[i], line_length=51))
        print(line)

    def handle_input(self):
        """Handle user input. Fetch relevant response."""

        response = self.fetch_response()
        if response in self.player_menu_responses:
            self.player_menu_table[response]()
        else:
            print("Invalid response. Type valid number.")


    def fetch_response(self):
        """Fetch the player response."""
        player_response = input("Response: ")
        return player_response

    def check_quests(self):
        """Check if quests need to be updated."""
        ongoing_quest_names = list(self.player.ongoing_quest_list.keys())

        if len(list(ongoing_quest_names)) == 0:
            pass
        else:
            for quest_name in ongoing_quest_names:
                self.player.ongoing_quest_list[quest_name].check_quest()
    
    # ------------------------------------- All player response options -------------------------------------
    def move_response(self):
        """Move player to new location."""
        self.player.move()

    def inventory_response(self):
        """Show inventory options."""
        while True:
            print("Select -- 1 Inventory -- 2 Equipped -- 3 Exit --")
            response = self.fetch_response()
            
            if response not in self.inventory_menu_responses:
                print("Type 1, 2 or 3\n")

            if response == "1":
                self.player.run_inventory_interaction(self.game_data["items"])
            elif response == "2":
                self.player.run_equip_interaction()
            elif response == "3":
                break
            
    def interactions_response(self):
        """Fetch the interaction response and run it if valid."""
        interactions = self.player.area_data["interactions"]
        response = self.show_interactions(interactions)

        if response == "Exit":
            pass

        if response in interactions.keys():
            interactions[response].run_logic()

        if self.player.dead == True:
            self.game_running = False

    def quests_response(self):
        """Open quest menu and run valid quest action."""
        while True:
            print("Select -- 1 Completed -- 2 Ongoing -- 3 Exit --")
            response = self.fetch_response()

            if response not in self.quest_menu_responses:
                print("Type 1, 2 or 3.")

            if response == "1":
                self.player.view_completed_quests()
            elif response == "2":
                self.player.view_ongoing_quests()
            elif response == "3":
                break

    def stats_response(self):
        """View player stats."""
        self.player.view_stats()

    def save_exit_response(self):
        """Close game and save state."""
        self.game_running = False

        script_filepath = os.path.abspath(__file__)
        saved_state_filepath = os.path.join(script_filepath, "..", "..", "saved_states\\savegame.pkl")
        self.save_game(saved_state_filepath)

    # ------------------------------------- Engine utils ------------------------------------- #
    # To be moved to somewhere else
        
    def show_interactions(self, interactions):
        """Show interactions.
        
        Args:
            interactions: Input interactions
            
        Returns:
            The corresponding interaction."""

        interaction_vals = {"0":"exit"}

        avail_interactions = list(interactions.keys())

        print("Select interaction: ")
        print("0 : Exit")
        for i, interaction in enumerate(avail_interactions[1:]):
            if interaction != "":
                print(f"{i + 1} : {interaction}")
                interaction_vals[str(i + 1)] = interaction

        while True:
            response = self.fetch_response()
            if response not in list(interaction_vals.keys()):
                print("Invalid input. Input valid number for the response.")
                continue
            else:
                break
        
        interaction_response = interaction_vals[response]

        return interaction_response



    def return_equipped_names(self):
        """Return the string names of equipped items.
        
        Args:
            None
            
        Returns:
            A tuple of the string names of the equipped items."""

        helmet_vals = self.player.equipped_helmet
        chestplate_vals = self.player.equipped_chestplate
        weapon_vals = self.player.equipped_weapon
        ring_vals = self.player.equipped_ring
        
        if helmet_vals != None:
            helmet = helmet_vals.item_name
        else:
            helmet = None

        if chestplate_vals != None:
            chestplate = chestplate_vals.item_name
        else:
            chestplate = None

        if weapon_vals != None:
            weapon = weapon_vals.item_name
        else:
            weapon = None

        if ring_vals != None:
            ring = ring_vals.item_name
        else:
            ring = None
        
        equipped_items = (helmet, chestplate, weapon, ring)
        return equipped_items

    def fill_interaction_gaps(self, interactions_input):
        """Fill any interactions gap.
        
        Args:
            interactions_input: The interactions input as a list.
            
        Returns:
            A list of interactions with spaces filled if length of interactions
            list is not 6. Else just return the original interactions list."""
        
        if len(interactions_input) != 6:
            missing_spaces = 6 - len(interactions_input)

            for _ in range(missing_spaces):
                interactions_input.append("")

            return interactions_input

        return interactions_input
    
    
if __name__ == "__main__":

    engine = Engine()    
    engine.set_player_settings()



            



