import time

from src.data.locations.windengard.windengard_npcs import WindergardNPCs

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
        
    # ----------------- Set up nodes ----------------- #

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
        
        Args:
            org_node: The front node.
            new_node: The back node."""
        self.dialogue_nodes[org_node].append(new_node)

    # ----------------- Dialogue flow ----------------- #
    
    def run_node(self):
        """Recursion method to call next node until reaching an end node where the 
        current_node_pos will be set to None to end the recursive cycle."""
        if self.current_node_pos != None:
            self.run_current_node_logic()
            self.return_next_node()
            self.run_node()

    def run_current_node_logic(self):
        """Run the logic of the current node."""

        # Extract the current node input - usually string
        # This string will either be dialogue text for
        # npc_dialogue nodes, player_dialogue nodes
        # or end_dialogue nodes. If the node is to run
        # a special function it will provide the input
        # to fetch the special function from the NPC class.
        current_node_input = self.current_node_pos[0]
        current_node_function = self.current_node_pos[1]

        # Run relevant node logic.
        if current_node_function == self.run_special_function:
            current_node_function(current_node_input)
        elif current_node_function == self.end_dialogue:
            self.run_end_node()
        else:
            current_node_function(current_node_input)

    def return_next_node(self):
        """A method to return the values of the next node.
        
        If next node is a straight node, length of node options will
        be one.
        
        If next node is empty, hence the end of the dialogue, set
        current_node_pos to None to end the recursion cycle.
        
        If next node is multi node, the length of node options will
        be greater than one. Run the return_multi_node method."""
        next_node_options = self.retrieve_node_options()
        
        # If an end dialogue node has been activated, the 
        # current_node_pos will be set to None hence
        # retrieve_node_options will return None.
        # Simply return to end this function logic.
        if next_node_options == None:
            return

        # If len next_node_options is 0, hence no further logic to be
        # done simply set the current_node_pos to None to end the 
        # run_node loop.
        if len(next_node_options) == 1:
            self.return_straight_node(next_node_options)
        elif len(next_node_options) == 0:
            self.current_node_pos = None
        elif len(next_node_options) > 1:
            self.return_multi_node(next_node_options)

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
        if self.current_node_pos != None:
            options = self.dialogue_nodes[self.current_node_pos]
            return options

    def return_straight_node(self, next_node_options):
        """Return the next node by setting the current_node_pos to 
        next node.

        Args:
            next_node_options: The next node options.
            
        Returns:
            None"""
        

        # Return the next node
        self.current_node_pos = next_node_options[0]

    def run_end_node(self):
        """Run an end node to end the dialogue. Runs the end dialogue
        and set the current_node_pos to None.
        
        Args:
            None
            
        Returns:
            None"""
        
        self.dialogue_player(self.current_node_pos[0])
        self.current_node_pos = None

    def return_multi_node(self, next_node_options):
        """Run a multi node, where there are multiple node options.
        The node type of the node options of multi nodes are always player
        dialogue. Special function node types will lead on from the corresponding
        node option.

        Multi nodes simply display the options, it does not run any of the logic.
        After displaying the options, and taking the input, the input will be
        aligned with chosen node option. From there a straight node will be run,
        which will be a player dialogue which then leads to the relevant option.
        
        Args:
            None

        Returns:
            """
        
        # Looking at the current node which is a multi node, get all the text
        # If want to edit and not display the text in future this is where you can edit
        # the logic. This text is the player dialogue text.

        raw_responses = [data[0] for data in next_node_options]

        # Enumerate the responses and display them.
        chat_responses = {str(num): resp for num, resp in enumerate(raw_responses) }
        self.list_chat_options(chat_responses)
        response_options = chat_responses.keys()

        # Check that a response is valid - a number which corresponds to one of the 
        # player dialogues.
        while True:
            response = input("Response: ")
            if response not in response_options:
                print("Invalid option. Type valid number.")
                continue
            break
        
        # Link the response to the node in a dictionary so it can be accessed.
        # Then get the node text that corresponds to the node.
        current_node_options = {resp: (resp, node_function) for resp, node_function in next_node_options}
        node_text = chat_responses[response]
        # Set the next node to the selected player dialogue. Essentially will run this as a straight node
        # in the next node iteration.
        self.current_node_pos = current_node_options[node_text]
        

    # ----------------- Node types ----------------- #

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
            node_input_value: Node input values match to the corresponding special function.
            
        Returns:
            None"""
        
        special_function = self.special_functions[node_input_value]
        
        pulled_function = special_function(node_input_value)
        pulled_function()

    def end_dialogue(self):
        """Placeholder method for end_dialogue. Does nothing but
        makes ensures all nodes have same format."""
        pass

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
    npcs = WindergardNPCs(item_database=None, player_reference=None)

    old_man = npcs.npc_packages("oldman")
    old_man.run_dialogue(dialogue_active=True)

    def get_method(type):
        def special_function():
            items = {"1":"test", "2":"test"}

            for i, item in items.items():

                print(i, item)

        if type == "buy_items":
            return special_function
        
    dialogue = Dialogue()


    dialogue.set_special_functions({"buy_items": get_method})

    # Dialogue below
        
    a = ("Blacksmith: Hello guv how can I help you?", dialogue.dialogue_npc)
    b = ("I would like to buy something.", dialogue.dialogue_player)
    c = ("Nothing.", dialogue.end_dialogue)
    d = ("buy_items", dialogue.run_special_function)
    e = ("End d")
    

    dialogue.initialise_node(a)
    dialogue.add_dialogue_node(b)
    dialogue.add_dialogue_node(c)
    dialogue.add_dialogue_node(d)

    dialogue.add_dialogue_edge(a, b)
    dialogue.add_dialogue_edge(a, c)
    dialogue.add_dialogue_edge(b, d)

    # dialogue.display_dialogue()

    dialogue.run_dialogue()