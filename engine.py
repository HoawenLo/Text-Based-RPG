import pickle
import os

from text_manipulation.text_manipulation import *
from data.game_data import game_data


# Connects the data to the player and handles input.

class Engine:

    def __init__(self):

        # ----------------------- Intialisation variables ----------------------- #

        self.player = None
        self.game_data = game_data

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
            print("Select option -- 1 play -- 2 lore -- 3 exit -- ")
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

    def set_player_settings(self):
        """Initialise the new start state for the player."""

        player = self.game_data["player"]

        self.player = player(base_health=15, 
                             base_attack=1, 
                             base_defence=0, 
                             level=1, 
                             current_location=self.game_data["locations"]["windergard"])
        
        # to be updated
        
        self.player.current_area = "Caravan"
        self.player.location_data = self.player.current_map.all_locations[self.player.current_location]

        welcome_text = "You arrive in Windengard, welcomed by an old man."
        text_crawl(welcome_text)

        # tutorial
    
    # ------------------------------------- Game state -------------------------------------

    def play(self):
        """Run the play option."""
        
        if os.path.isfile("../saved_states/savegame.pkl"):
            while True:
                print("Start a new game? yes/no\n")
                response = self.fetch_response()
                
                if response != "yes" or response != "no":
                    print("Invalid response. Type yes or no.")
                
                if response == "yes":
                    self.game_running = True
                    self.load_new_game()
                    self.run_game()
                    break
                elif response == "no":
                    self.player = self.load_saved_game("../saved_states/savegame.pkl")
                    self.game_running = True
                    self.run_game()
                    break
        else:
            self.load_new_game()
            self.game_running = True
            self.run_game()

    def load_new_game(self):
        """Load a new game."""

        # self.load_title_screen()
        # self.load_intro_text()
        self.set_player_settings()

    def run_game(self):
        while self.game_running:
            self.show_ingame_menu()
            self.handle_input()
            self.check_quests()

    def save_game(self, filename):
        """"Save game with pickle."""

        with open(filename, "wb") as file:
            pickle.dump(self.player, file)
        print("Game saved!")

    def load_saved_game(self, filename):
        """Load a save pickle file."""

        with open(filename, "rb") as file:
            loaded_game = pickle.load(file)
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

        available_interactions = self.player.area_data["interactions"].keys()

        print(f"Health: {self.player.health}    Current Location: {self.player.current_location}    Gold: {self.player.gold}    Inventory space: {self.player.inventory_size} / {self.player.max_inventory_size}")
        print(line)
        print(combine_characters(f"Helmet {self.player.inventory['helmet']}", f"Leggings: {self.player.inventory['leggings']}"))
        print(combine_characters(f"Chestplate: {self.player.inventory['chestplate']}", f"Ring: {self.player.inventory['ring']}"))
        print(line)
        for i in range(len(self.player_menu_options)):
            print(combine_characters(self.player_menu_options[i], available_interactions[i]))
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
        ongoing_quests = self.player.ongoing_quest_list.keys()

        if len(list(ongoing_quests)) == 0:
            pass
        else:
            for quest in ongoing_quests:
                quest.check_quest()
    


    
    # ------------------------------------- All player response options -------------------------------------
    def move_response(self):
        """Move player to new location."""
        self.player.move()

    def inventory_response(self):
        """Show inventory options."""
        while True:
            print("Select -- 1 Inventory -- 2 Equipped -- 3 Exit --\n")
            response = self.fetch_response()
            
            if response not in self.inventory_menu_response:
                print("Type 1, 2 or 3\n")

            if response == "1":
                self.player.inventory_menu()
            elif response == "2":
                self.player.equipped_menu()
            elif response == "3":
                break
            
    def interactions_response(self):
        """Fetch the interaction response and run it if valid."""
        response = self.fetch_response()
        interactions = self.player.area_data["interactions"]

        if response not in interactions.keys() or response == "":
            print("Invalid interaction")

        if response in interactions.keys():
            interactions[response].run_logic()

        if self.player.dead == True:
            self.game_running = False

    def quests_response(self):
        """Open quest menu and run valid quest action."""
        while True:
            print("Select -- 1 Completed -- 2 Ongoing -- 3 Exit --\n")
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
        self.save_game("saved_states/savegame.pkl")
        
            
        



            



