from random import randint
import time

class Npc:
    """The base general npc class. This type of npc provides dialogue to the player."""
    def __init__(self, dialogue, name):
        self.npc_type = "general"
        self.name = name
        self.dialogue_text = dialogue
        self.dialogue_active = False

    def run_dialogue(self, dialogue_active):
        if callable(self.dialogue_text):
            self.dialogue_text(dialogue_active)
        else:
            return "Dialogue error."

class Quest(Npc):
    """Quest npcs update their dialogue as a quest progresses. They will interact with the quest module in the higher level location file."""
    def __init__(self, dialogue, name, quest_reference):
        super().__init__(dialogue, name)

        self.npc_type = "quest"
        self.quest_reference = quest_reference

    def add_quest(self, player_reference):
        pass
        

class SellTrader(Npc):
    """Trader npcs provide products and services to the player. They will with funnel into the locations module, 
    which will allow interactions with items in the data module."""
    def __init__(self, dialogue, name, products, item_data):
        super().__init__(dialogue, name)

        self.npc_type = "trader"
        self.products = products
        self.item_database = item_data.item_database
        self.character_reference = None

    def show_products(self):
        """Display the products available for sale.
        
        Args:
            None
        
        Returns:    
            None"""
        
        for index, product_tag in self.products.items():
            product = self.item_database[product_tag]
            print(f"{index} {product.item_name} : {product.item_description} : {product.value} gold")
        
    def buy_items(self, item_input):
        """Initiate a buy method for the character.
        
        Args:
            item_input: The item input as a string."""
        
        all_items = list(self.item_database.keys())

        if item_input in all_items:
            fetched_item = self.item_database[item_input]
            self.character_reference.buy_item(fetched_item)

    def run_buy_response(self):
        """Run a input to get the player buy response.
        
        Args:
            None
            
        Returns:
            A string, the response of the player which corresponds
            to an item."""

        response = input("State the number of the item you would like to purchase or type 0 to exit.\n")

        return response

    def fetch_item(self, item_tag):
        """Fetch item from database.
        
        Args:
            item_name: The item name that will be used to access the value 
            from the item database dictionary.
            
        Returns:
            An object of the item."""
        
        product_tag = self.products[item_tag]
        fetched_item = self.item_database[product_tag]

        return fetched_item

    def continue_interaction(self):
        """Method to initiate whether to continue buy or sell interaction.
        
        Args:
            None
            
        Returns:
            Returns true to finish interaction, whilst returns false to
            continue interaction."""
        
        while True:
            response = input("Anything else: 1 yes / 2 no\n")

            if response == "1" or response == "2":
                break
            
            print("Invalid response, type 1 or 2.")

        if response == "1":
            return True
        elif response == "2":
            return False


    def display_sellable_items(self, player_inventory_items):
        """Calculates the value of items in the inventory that the trader is willing to buy.
        Then displays these sellable items.
        
        Args:
            player_inventory_items: A reference to the player's inventory.
            
        Returns:
            A dicitonary of sellable items."""
        
        sellable_items = {}

        print("Items that can be sold: ")
        for i, inventory_item in enumerate(player_inventory_items):
            sellable_items[str(i + 1)] = inventory_item
            print(f"{i + 1} {inventory_item.item_name} : {inventory_item.item_description} : : {inventory_item.value // 2} gold")

        return sellable_items

    def run_sell_response(self):
        """Run a input to get the player sell response.
        
        Args:
            None
            
        Returns:
            A string, the response of the player which corresponds
            to an item."""

        response = input("State the number of the item you would like to sell or type 0 to exit.\n")

        return response

    def sell_items(self, item_input):
        """Initiate a sell method for the character.
        
        Args:
            item_input: The item input as a string."""
        
        all_items = list(self.item_database.keys())

        if item_input in all_items:
            fetched_item = self.item_database[item_input]
            self.character_reference.sell_item(fetched_item)

    def trader_methods(self, method="buy_items"):
        """Holds all trader methods.
        
        Args:
            method: The method to retrieve. If buy_items,
            return the purchase sequence. If sell_items, return
            the sell sequence
            
        Returns:
            The corresponding trading method."""
        
        if method != "buy_items" or method != "sell_items":
            raise ValueError(f"Invalid method input. Must be buy_items or sell_items, instead input is {method}.")
        
        def run_purchase_sequence():
            """Run a buy sequence. Buy sequence consists of a while loop with
            the following order.
            
            Show products.
            Request for a response.
            Either buy item or exit.
            If buy item run buy item method.
            Request to continue the loop, if so go to the start.
            
            Args:
                None
                
            Returns:
                None"""
            
            while True:
                self.show_products()
                response = self.run_buy_response()

                if response == "0":
                    break

                if response not in self.products.keys():
                    print("Invalid number.")
                    continue
                
                fetched_item  = self.fetch_item(response)
                self.buy_items(fetched_item)
                continue_interaction_resp = self.continue_interaction()

                if continue_interaction_resp:
                    break

        def run_sell_sequence():
            """Run a sell sequence. Sell sequence consists of a while loop with
            the following order.
            
            Show player inventory.
            Request for a response.
            Either sell item or exit.
            If sell item run sell item method.
            Request to continue the loop, if so go to the start.
            
            Args:
                None
                
            Returns:
                None"""
            
            while True:
                sellable_items = self.display_sellable_items()
                response = self.run_sell_response()

                if response == "0":
                    break

                if response not in sellable_items.keys():
                    print("Invalid number.")
                    continue
                
                fetched_item  = self.fetch_item(response)
                self.sell_items(fetched_item)
                continue_interaction_resp = self.continue_interaction()

                if continue_interaction_resp:
                    break

        if method == "buy_items":
            return run_purchase_sequence
        elif method == "sell_items":
            return run_sell_sequence

    def run_trading_dialogue(self, dialogue_active):
        """Run trading dialogue. This is a special type of dialogue which allows buy/sell interactions with the player."""
        self.dialogue_text(dialogue_active, self.trader_methods, self.item_database, self.character_reference)

class Combat(Npc):

    def __init__(self, dialogue, name, base_health, attack, defence,  skill_level, common_exp_ranges):
        super().__init__(dialogue, name)

        # NPC type

        self.npc_type = "combat"

        # NPC stats
        self.current_health = base_health
        self.base_health = base_health
        self.attack = attack
        self.defence = defence
        self.skill_level = skill_level

        # Rewards for defeating the npc
        self.exp_ranges = common_exp_ranges
        self.exp_output = self.exp_ranges[self.skill_level]
        self.gold_range = (int((1.5 ** self.skill_level - 1) * 2), int((1.5 ** self.skill_level) * 2))

        # Status
        self.alive = True
        self.available = False

    def calculate_damage_inflicted(self):
        """Calculate the damage that is inflicted on the target (player).
        
        Args:
            randint: Random integer function is used to add randomness 
            to the damage values."""
        offset_value = randint(0, 3)

        if self.skill_level > 3:
            damage = self.attack - self.defence + offset_value
        else:
            damage = self.attack - self.defence - offset_value

        if damage < 0:
            damage = 0

        return damage

    def calculate_damage_taken(self):
        """Calculate the damage that is inflicted by the target (player).
        
        Args:
            randint: Random integer function is used to add randomness 
            to the damage values."""
        if self.skill_level > 5:
            offset_value = randint(1, 5)
            damage = self.attack - self.defence - offset_value 
        
        elif self.skill_level < 5:
            offset_value = randint(0,3)
            damage = self.attack - self.defence - offset_value
        
        if damage < 0:
            damage = 0

        return damage

    def take_damage(self):
        """Take damage during combat. Sets NPC to dead if defeated.
        
        Args:
            randint: Randint function to provide random values to calculate the damage."""

        damage = self.calculate_damage_inflicted()

        self.current_health -= damage

        if self.current_health < 0:
            self.current_health = 0
            self.alive = False

    def inflict_damage(self, target):
        """Inflict damage on target.
        
        Args:
            target: The target that damage will be inflicted on. The player.
            randint: Randint function to provide random values to calculate the damage."""
        
        damage = self.calculate_damage_inflicted()

        target.current_health -= damage

    def reset_health(self):
        """Reset the NPC's health to its original value after being defeated."""
        self.current_health = self.base_health

    def set_alive(self):
        """Reset the npc to its original state."""
        self.alive = True

    def return_exp(self):
        """Returns the exp after being defeated by player 
        Exp amount is calculated based off the skill level of
        npc from the common exp range attribute.
        
        Args:
            randint: Used to randomise the exp output."""
        
        exp_amount = randint(self.exp_output[0], self.exp_output[1])
        return exp_amount

    def return_gold(self):
        """Returns the gold amount after being defeated by player 
        Gold amount is calculated based off the skill level of
        npc from the gold range attribute.
        
        Args:
            randint: used to randomise the gold output."""
        
        gold_amount = randint(self.gold_range[0], self.gold_range[1])
        return gold_amount
    
    def check_on_condition(self, on_condition):
        """Checks the availability condition. If satisfied makes 
        available or unavailable. Makes the npc available for combat. 
        Sometimes there will be a cooldown or a specific trigger 
        required to make npc available."""

        if on_condition:
            self.available = True
        
    def check_off_condition(self, off_condition):
        """Turns off the availability of the NPC for combat."""

        if off_condition:
            self.available = False

    def run_combat_sequence(self, player):
        """Run a combat sequence.
        
        Args:
            player: A reference to player object to access
            player methods."""

        self.take_damage()
        self.inflict_damage(player)

        if self.current_health <= 0:
            print(f"{self.name} defeated!")
            exp_reward = self.return_exp()
            gold_reward = self.return_gold()

            player.gain_exp(exp_reward)
            player.gold += gold_reward

            player.add_defeated_npc(self)

            self.reset_health()
        elif player.current_health <= 0:
            print("You have been defeated!")
            player.dead = True
            player.in_combat = False

            
class Dialogue:

    def __init__(self):
        self.dialogue_nodes = {}

    # ----------------- Run dialogue ----------------- #

    def run_dialogue(self):
        """Run the dialogue by starting the recursion method
        run_node()
        
        Args:
            None
            
        Returns:
            None"""
        self.run_node()
        
    # ----------------- Add dialogue node ----------------- #

    def initialise_node(self, dialogue_data):
        """Initialise the node. This must be done for the
        first node to set the current_node_pos to the initial
        dialogue.
        
        Args:
            dialogue_data: The first node data. Which is a tuple
            of the format ("Dialogue text", dialogue.dialogue_npc).
            
        Returns:
            None"""
        
        if not isinstance(dialogue_data, tuple):
            raise TypeError(f"Input dialogue data must be a tuple. It is instead is a {type(dialogue_data)}. Dialogue data is {dialogue_data}.")
        if len(dialogue_data) != 2:
            raise ValueError(f"Length of dialogue data is not 2. Initial dialogue will always be of the format ('Dialogue text', dialogue.dialogue_npc). Instead input dialogue is {dialogue_data}")

        self.add_dialogue_node(dialogue_data)
        self.current_node_pos = dialogue_data

    def add_dialogue_node(self, dialogue_data):
        """Add a dialogue node to the dictionary which stores all nodes.
        
        Args:
            dialogue_data: The data for the dialogue node. Will be a tuple of format
            ("dialogue text", dialogue.method) or if response node will be similar
            but multiples of this format.
            
        Returns:
            None"""
        if dialogue_data not in self.dialogue_nodes:
            self.dialogue_nodes[dialogue_data] = []

    def add_dialogue_edge(self, dialogue_data_one, dialogue_data_two):
        """Add a dialogue edge to connect two nodes. Check dialogue nodes
        exist as well, if not create them.
        
        Args:
            dialogue_data_one: The front node to connect.
            dialogue_data_two: The back node to connect the front node to."""
        self.add_dialogue_node(dialogue_data_one)
        self.add_dialogue_node(dialogue_data_two)

        self.connect_nodes(dialogue_data_one, dialogue_data_two)

    def connect_nodes(self, org_node, new_node):
        """Connect the nodes. Nodes connect from org_node
        to new_node.

        If length of new_node is 2, means it is a straight node hence
        simple append to edges of the org_node.

        Otherwise it will be a response node hence iterate through
        and append all.
        
        Args:
            org_node: The front node.
            new_node: The back node."""
        if len(new_node) == 2:
            self.dialogue_nodes[org_node].append(new_node)
        else:
            for data in new_node:
                if isinstance(data, tuple):
                    self.dialogue_nodes[org_node].append(data)
                else:
                    self.dialogue_nodes[org_node].append((data))

    # ----------------- Dialogue flow ----------------- #
    
    def run_node(self):
        """Recursion method to call next node until reaching an end node where the 
        current_node_pos will be set to None to end the recursive cycle."""
        if self.current_node_pos != None:
            self.return_next_node()
            input("")
            self.run_node()

    def return_next_node(self):
        """A method to return the values of the next node.
        
        If next node is a straight node, length of node options will
        be one.
        
        If next node is empty, hence the end of the dialogue, set
        current_node_pos to None to end the recursion cycle.
        
        If next node is response node, the length of node options will
        be greater than one. Run the run_response_node method."""
        node_options = self.retrieve_node_options()

        if len(node_options) == 1:
            self.run_straight_node(node_options)
        elif len(node_options) == 0:
            self.run_end_node()
        else:
            self.run_response_node(node_options)

    def run_straight_node(self, node_options):
        """Running a straight node moves straight away to the next
        node option as there is only one option.
        
        First fetch the current node input and then run the current
        node function.

        Next get the next node and return it so it can be passed.

        Args:
            node_options: The next node options.
            
        Returns:
            None"""
        current_node_input = self.current_node_pos[0]
        current_node_function = self.current_node_pos[1]

        print("current node_function", current_node_function, "current node input", current_node_input)

        if current_node_function == self.run_special_function:
            current_node_function(current_node_input)
        elif current_node_function == self.end_dialogue:
            self.dialogue_player(current_node_input)
        else:
            current_node_function(current_node_input)

        self.get_next_single_node(node_options)
        
    
    def run_response_node(self, node_options):
        """Run a response node. Response nodes are nodes which contain
        responses. Unlike a straight node which only has one option.
        
        Args:
            node_options: The next node options. This is where the 
            responses will be sourced from.
            
        Returns:
            None"""
        print(f"run_response_node current_node_pos: {self.current_node_pos[1]}")

        # pull out responses and show them
        current_node_input = self.current_node_pos[0]
        current_node_function = self.current_node_pos[1]
        current_node_function(current_node_input)

        self.show_responses(node_options)

    def run_end_node(self):
        """Run an end node. If the current node has no edges."""
        current_node_function = self.current_node_pos[1]
        current_node_function()


    # ----------------- Retrieving node data ----------------- #
    
    def retrieve_node_options(self):
        """Retrieves the next node options. If the next node is a
        response node, you will have multiple values in the node,
        otherwise the node is a straight node and will just be the
        first value of the list.
        
        Args:
            None
            
        Returns:
            The next node options."""
        options = self.dialogue_nodes[self.current_node_pos]
        return options

    def get_next_single_node(self, node_options):
        """Get the next single node which is a node with only one value.
        
        Args:
            node_options: The next node options.
            
        Returns:
            None"""
        if len(node_options) != 0:
            next_node = node_options[0]
            self.current_node_pos = next_node

    # ----------------- Dialogue building blocks ----------------- #

    def dialogue_npc(self, dialogue):
        """The npc dialogue. Text crawl the dialogue.
        
        Args:
            dialogue: The dialogue, must be a string.
            
        Returns:
            None"""
        
        if not isinstance(dialogue, str):
            raise TypeError(f"Input dialogue is not str datatype. Instead dialogue is {type(dialogue)} datatype. Dialogue is {dialogue}.")
        self.word_crawl(dialogue)

    def dialogue_player(self, dialogue):
        """The player dialogue. Add adventurer tag to the front.
        Then text crawl the dialogue.
        
        Args:
            dialogue: The dialogue, must be a string.
            
        Returns:
            None"""
        
        if not isinstance(dialogue, str):
            raise TypeError(f"Input dialogue is not str datatype. Instead dialogue is {type(dialogue)} datatype. Dialogue is {dialogue}.")
        player_dialogue = self.add_adventurer(dialogue)
        self.word_crawl(player_dialogue)

    def set_special_functions(self, special_functions):
        """Set the special functions to be accessed later.
        
        Args:
            special_functions: Must be a dictionary with a string key which matches
            the special function.
            
        Return:
            None"""
        
        if not isinstance(special_functions, dict):
            raise TypeError(f"special_functions is not dictionary type. Instead is type {type(special_functions)}. Input is {special_functions}.")
        
        self.special_functions = special_functions

    def run_special_function(self, node_input_value):
        """Run a special utility function such as show items for a trader npc.
        
        Args:
            function: The input function to be run.
            node_input_values: Node input values match to the corresponding special function.
            
        Returns:
            None"""
        
        print("running special function", self.special_functions, "node_input_value", node_input_value)

        print(self.special_functions)

        special_function = self.special_functions[node_input_value]
        
        pulled_function = special_function(node_input_value)
        pulled_function()
        
        
    def show_responses(self, node_options):
        """Show the possible player responses. Sourced from the next node that is pointed at.
        Node is of the format:
        (("text option one", option_one_function), ("text option two", option_two_function) dialogue.show_responses).
        Where the dialogue.show_response is the dialogue.show_response method.
        
        Chat responses are then numbered with enumerate and then list options method is used to print out the
        potential chat responses.

        Logic then goes on to check if the response given is valid.

        Finally get the node that the player responded to and set it to the current node position.

        Args:
            node_options: The node options being pointed at. Must be a list of tuples.

        Returns:
            None
        """

        if not isinstance(node_options, list):
            raise TypeError(f"Node options is not a list. Instead type is {type(node_options)}. node_options is {node_options}.")

        raw_responses = [data[0] for data in node_options[:-1]]
        chat_responses = {str(num): resp for num, resp in enumerate(raw_responses) }
        self.list_chat_options(chat_responses)
        response_options = chat_responses.keys()

        while True:
            response = input("Response: ")
            if response not in response_options:
                print("Invalid option. Type valid number.")
                continue
            break
        
        next_node = node_options[int(response)]
        self.dialogue_player(next_node[0])

        self.current_node_pos = next_node

    def end_dialogue(self):
        """Set the current node postion to None to end the 
        dialogue.
        
        Args:
            None
            
        Returns:
            None"""
        
        self.current_node_pos = None


    # ----------------- Viewing Nodes ----------------- #

    def display_dialogue(self):
        """Display the dialogue. This is used to debug.
        
        Args:
            None
            
        Returns:
            None"""
        for node, neighbors in self.dialogue_nodes.items():
            print(f"{node}: {neighbors}")

    # ----------------- Text manipulation ----------------- #
            
    def word_crawl(self, text, line_length=60, text_speed=0.1):
        """Used to crawl text. Crawls words instead of 
        single characters.
        
        Args:
            text: The sentence to be crawled.
            line_length: Sets the length of the line.
            If has a large body of text, will move 
            onto next line if line length reached."""

        words = text.split()
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= line_length:
                current_line += word + " "
            else:
                print(current_line)
                current_line = word + " "
                time.sleep(text_speed)

            print(current_line, end="\r")
            time.sleep(text_speed)

        print(current_line)

    def add_adventurer(self, text):
        """Add adventurer to the start of the next.
        
        Args:
            text: The text to add adventurer to."""
        return "Adventurer: " + text
    
    def list_chat_options(self, chat_options):
        """Takes a dictionary of chat options and prints it.
        
        Args:
            chat_options: The chat options to print."""
        
        for num, text in chat_options.items():
            display_text = num + ": " + text
            print(display_text)

            

if __name__ == "__main__":

    def trader_dialogue_package(*args):
        """Dialogue package for trader.
        
        Args:
            *args: Accepts any number of arguments as 
            run_dialogue method for NPC varies.

        Returns:
            None
        """

        trader_dialogue = Dialogue()

        if len(list(args)) == 4:
            special_functions = {"show_products":args[1]}
            trader_dialogue.set_special_functions(special_functions)

        # Dialogue below
            
        a = ("Trader: Hello", trader_dialogue.dialogue_npc)
        b = ("Hello", trader_dialogue.dialogue_player)
        c = ("NPC: How can I help?", trader_dialogue.dialogue_npc)
        d = ((("end", trader_dialogue.end_dialogue), ("show_products", trader_dialogue.run_special_function), trader_dialogue.show_responses))
        e = ("end", trader_dialogue.end_dialogue)
        f = ("show_products", trader_dialogue.run_special_function)
        g = ("chat", trader_dialogue.dialogue_npc)
        h = ("buy_items")

        trader_dialogue.initialise_node(a)
        trader_dialogue.add_dialogue_node(b)
        trader_dialogue.add_dialogue_node(c)
        trader_dialogue.add_dialogue_node(d)
        trader_dialogue.add_dialogue_node(e)
        trader_dialogue.add_dialogue_node(f)
        trader_dialogue.add_dialogue_node(g)

        trader_dialogue.add_dialogue_edge(a, b)
        trader_dialogue.add_dialogue_edge(b, c)
        trader_dialogue.add_dialogue_edge(c, d)
        trader_dialogue.add_dialogue_edge(d, e)
        trader_dialogue.add_dialogue_edge(d, f)
        trader_dialogue.add_dialogue_edge(d, g)
        trader_dialogue.add_dialogue_edge(f, e)
        trader_dialogue.add_dialogue_edge(g, e)

        trader_dialogue.run_dialogue()

    class test_items:

        def __init__(self, item_name, value, item_description):
            self.item_name = item_name
            self.value = value
            self.item_description = item_description

    test = test_items("test", 2, "desc")
    test_two = test_items("test two", 3, "desc 2")


    products = {"test":test, "test2":test_two}


    test_npc = SellTrader(trader_dialogue_package, "test_npc", products=products, item_database=None)
    test_npc.run_trading_dialogue(dialogue_active=True)

        
