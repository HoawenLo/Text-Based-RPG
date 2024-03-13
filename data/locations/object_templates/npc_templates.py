from random import randint

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
    def __init__(self, dialogue, name, products):
        super().__init__(dialogue, name)

        self.npc_type = "trader"
        self.products = products
        self.character_reference = None

    def show_products(self):
        """Display the products available for sale."""
        for product in self.products.values():
            print(f"{product.item_name} : {product.item_description} : {product.value} gold")

    def run_trading_dialogue(self, dialogue_active):
        """Run trading dialogue. This is a special type of dialogue which allows buy/sell interactions with the player."""
        self.dialogue_text(dialogue_active, self.show_products, self.items)


class BuySellTrader(SellTrader):

    def __init__(self, dialogue, name, products):
        super().__init__(dialogue, name, products)

    def calculate_buy_values(self, player_inventory_items):
        """Calculates the value of items in the inventory that the trader is willing to buy. 
        
        Args:
            player_inventory_items: A reference to the player's inventory."""
        
        print("Items that can be sold: ")
        for inventory_item in player_inventory_items:
            print(f"{inventory_item.item_name} : {inventory_item.value // 2} gold")

    def run_trading_dialogue(self, dialogue_active):
        self.dialogue_text(dialogue_active, self.show_products, self.calculate_buy_values, self.items, self.character_reference)

    

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

    def __init__(self, text_crawl, add_adventurer, list_options):
        self.text_crawl = text_crawl
        self.add_adventurer = add_adventurer
        self.list_options = list_options

        self.dialogue_nodes = {}

    # ----------------- Run dialogue ----------------- #

    def run_dialogue(self):
        self.run_node()
        
    # ----------------- Add dialogue node ----------------- #

    def initialise_node(self, dialogue_data):
        self.add_dialogue_node(dialogue_data)
        self.current_node_pos = dialogue_data

    def add_dialogue_node(self, dialogue_data):
        if dialogue_data not in self.dialogue_nodes:
            self.dialogue_nodes[dialogue_data] = []

    def add_dialogue_edge(self, dialogue_data_one, dialogue_data_two):
        self.add_dialogue_node(dialogue_data_one)
        self.add_dialogue_node(dialogue_data_two)

        self.connect_nodes(dialogue_data_one, dialogue_data_two)

    def connect_nodes(self, org_node, new_node):
        print("node", new_node)
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
        if self.current_node_pos != None:
            self.return_next_node()
            input("")
            self.run_node()

    def return_next_node(self):
        node_options = self.retrieve_node_options()

        print("node options", node_options)

        if len(node_options) == 1:
            self.run_straight_node(node_options)
        elif len(node_options) == 0:
            self.run_straight_node(node_options)
            self.current_node_pos = None
        else:
            self.run_response_node(node_options)

    def run_straight_node(self, node_options):
        """Running a straight node moves straight away to the next
        node option as there is only one option.
        
        First fetche the current node input and then run the current
        node function.

        Next get the next node and return it so it can be passed.

        Args:
            node_options: The next node options."""
        current_node_input = self.current_node_pos[0]
        current_node_function = self.current_node_pos[1]

        current_node_function(current_node_input)

        self.get_next_single_node(node_options)
        
    
    def run_response_node(self, node_options):
        print(node_options)


        current_node_function = self.current_node_pos[1]
        current_node_function(node_options)

    # ----------------- Retrieving node data ----------------- #
    
    def retrieve_node_options(self):
        """Retrieves the next node options. If the next node is a
        response node, you will have multiple values in the node,
        otherwise the node is a straight node and will just be the
        first value of the list."""
        options = self.dialogue_nodes[self.current_node_pos]
        return options

    def get_next_single_node(self, node_options):
        """Get the next single node which is a node with only one value.
        
        Args:
            node_options: The next node options."""
        if len(node_options) != 0:
            next_node = node_options[0]
            self.current_node_pos = next_node

    # ----------------- Dialogue building blocks ----------------- #

    def dialogue_npc(self, dialogue):
        self.text_crawl(dialogue)

    def dialogue_player(self, dialogue):
        player_dialogue = self.add_adventurer(dialogue)
        self.text_crawl(player_dialogue)

    def run_special_function(self, function):
        function()
        
    def show_responses(self, node_options):
        raw_responses = [data[0] for data in node_options]
        chat_responses = {num: resp for num, resp in enumerate(raw_responses) }
        self.list_options(chat_responses)
        response_options = chat_responses.keys()

        while True:
            response = input("Response: ")
            if response not in response_options:
                print("Invalid option. Type valid number.")
                continue
            break
        
        next_node = node_options[int(response) - 1]
        self.current_node_pos = next_node

    # ----------------- Viewing dialogue ----------------- #

    def display_dialogue(self):
        for node, neighbors in self.dialogue_nodes.items():
            print(f"{node}: {neighbors}")

if __name__ == "__main__":
    import sys

    filepath = r"C:\Users\Hoawen\Desktop\Programming\Python\Text based rpg\Alpha Version 2\text_manipulation"
    sys.path.append(filepath)

    from text_manipulation import word_crawl, add_adventurer, list_chat_options 

    dialogue = Dialogue(word_crawl, add_adventurer, list_chat_options)

    a = ("Test", dialogue.dialogue_npc)
    b = ("Test 2", dialogue.dialogue_player)
    c = ((("end", "end dialogue function"), ("show items", dialogue.run_special_function), ("chat", dialogue.dialogue_npc), dialogue.show_responses))

    print(len(a))

    dialogue.initialise_node(a)
    dialogue.add_dialogue_node(b)
    dialogue.add_dialogue_node(c)
    
    

    dialogue.add_dialogue_edge(a, b)
    dialogue.add_dialogue_edge(b, c)

    # dialogue.display_dialogue()

    dialogue.run_dialogue()

    
