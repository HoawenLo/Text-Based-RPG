from ..object_templates.npc_templates import *

class WindergardNPCs:

    def __init__(self, item_database, player_reference):
        self.npc_database = {}
        self.item_database = item_database
        self.player_reference = player_reference

    def dialogue_packages(self, npc_reference):
        """Holds the dialogue packages.

        Args:
            npc_reference: The npc reference refers to the dialogue package to fetch.

        Returns:
            A dialogue package which is a function containing the logic of the dialogue
            to run.
        """


        def blacksmith_dialogue_package(*args):
            """Dialogue package for blacksmith.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()


            if len(list(args)) == 4:
                special_functions = {"buy_items":args[1]}
                dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("Blacksmith: Hello guv how can I help you?", dialogue.dialogue_npc)
            b = ("Nothing.", dialogue.end_dialogue)
            c =  ("I would like to buy some items.", dialogue.dialogue_player)
            d = ("buy_items", dialogue.run_special_function)

            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(b)
            dialogue.add_dialogue_node(c)
            dialogue.add_dialogue_node(d)

            dialogue.add_dialogue_edge(a, b)
            dialogue.add_dialogue_edge(a, c)
            dialogue.add_dialogue_edge(c, d)

            dialogue.run_dialogue()

        def oldman_intro_dialogue_package(*args):
            """Dialogue package for oldman.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()


            if len(list(args)) == 2:
                special_functions = {"start_quest":args[1]}
                dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("Old man: Ah, a newcomer to Windengard! I sense the spark of adventure in your eyes. Welcome, young one. What brings you to our humble village?", dialogue.dialogue_npc)
            b = ("Thank you, sir. I've come in search of renown and fortune. There's talk of a grand quest and an ancient artifact.", dialogue.dialogue_player)
            c = ("Old man: The Heartstone, no doubt. A tale as old as time. Many have sought it, but few truly understand its mysteries. Be cautious, for the path to Astralhaven is fraught with challenges.", dialogue.dialogue_npc)
            d = ("Challenges, you say? What advice do you have for a novice like me?", dialogue.dialogue_player)
            e = ("Old man: Patience, young adventurer. Explore Windengard, learn its secrets, and forge bonds with its people. Each villager has a story, and knowledge is as valuable as any treasure. Before you rush off to Astralhaven, let the winds of fate guide you through our humble abode.", dialogue.dialogue_npc)
            f = ("Wise words, sir. Where do you recommend I begin?", dialogue.dialogue_player)
            g = ("Old man: Start with visiting the blacksmith, if you want to make it to Astralhaven you will need some good gear to get you through the dark forests.", dialogue.dialogue_npc)
            h = ("start_quest", dialogue.run_special_function)

            # Ensure node name is different to prevent it being an unintended mutli node.
            i = ("player_continue_input_1", dialogue.player_continue_response)
            j = ("player_continue_input_2", dialogue.player_continue_response)
            k = ("player_continue_input_3", dialogue.player_continue_response)
            l = ("player_continue_input_4", dialogue.player_continue_response)
            m = ("player_continue_input_5", dialogue.player_continue_response)
            n = ("player_continue_input_6", dialogue.player_continue_response)

            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(b)
            dialogue.add_dialogue_node(c)
            dialogue.add_dialogue_node(d)
            dialogue.add_dialogue_node(e)
            dialogue.add_dialogue_node(f)
            dialogue.add_dialogue_node(g)
            dialogue.add_dialogue_node(h)
            dialogue.add_dialogue_node(i)
            dialogue.add_dialogue_node(j)
            dialogue.add_dialogue_node(k)
            dialogue.add_dialogue_node(l)
            dialogue.add_dialogue_node(m)
            dialogue.add_dialogue_node(n)

            dialogue.add_dialogue_edge(a, i)
            dialogue.add_dialogue_edge(i, b)
            dialogue.add_dialogue_edge(b, j)
            dialogue.add_dialogue_edge(j, c)
            dialogue.add_dialogue_edge(c, k)
            dialogue.add_dialogue_edge(k, d)
            dialogue.add_dialogue_edge(d, l)
            dialogue.add_dialogue_edge(l, e)
            dialogue.add_dialogue_edge(e, m)
            dialogue.add_dialogue_edge(m, f)
            dialogue.add_dialogue_edge(f, n)
            dialogue.add_dialogue_edge(n, g)
            dialogue.add_dialogue_edge(g, h)

            dialogue.run_dialogue()

        def villager_ts_dialogue_package(*args):
            """Dialogue package for villager in the town square.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()

            # Dialogue below
                
            a = ("Villager: If you are looking to heal up you can go to the general store to purchase some consumables, or you can head to the inn to rest up.", dialogue.dialogue_npc)

            dialogue.initialise_node(a)

            dialogue.run_dialogue()

        def oldman_dialogue_package(*args):
            """Dialogue package for oldman. He provides advice on the game.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()

            # Dialogue below
                
            a = ("Old man: Hello how may I be of assistance?", dialogue.dialogue_npc)

            # ---------- Player Responses ---------- #
            b = ("Tell me about moving.", dialogue.dialogue_player)
            c = ("Tell me about using the inventory.", dialogue.dialogue_player)
            d = ("Tell me about using the interactions.", dialogue.dialogue_player)
            e = ("Tell me about using the quests.", dialogue.dialogue_player)
            f = ("Tell me about using the stats.", dialogue.dialogue_player)
            g = ("Tell me about using the saving game.", dialogue.dialogue_player)
            h = ("Sorry nothing.", dialogue.end_dialogue)

            # ---------- NPC Responses ---------- #
            i = ("Old man: To move your character, select the move option (number one), and then relevant location.", dialogue.dialogue_npc)
            j = ("Old man: The inventory option (number two) allows you to view your inventory, drop items, equip items and unequip items.", dialogue.dialogue_npc)
            k = ("Old man: Available interactions are listed on the player menu. You can select one of them by selecting the interact option.", dialogue.dialogue_npc)
            ka = ("Old man: Interactions include talking to NPCs, combat and environment interactions such as cutting trees.", dialogue.dialogue_npc)
            l = ("Old man: Select the quests option (number four) to see details for any ongoing or completed quests. This can provide you ideas on what to do next.", dialogue.dialogue_npc)
            m = ("Old man: Select the stats option (number five) to see your current stats. Attack increases the amount of damage you can do in combat, whilst defence reduces the damage taken.", dialogue.dialogue_npc)
            ma = ("Old man: As you complete quests and win duels you will level up, increasing your base health and attack.", dialogue.dialogue_npc)
            n = ("Old man: To save your game select option six. Your game will be saved and you can return at any time!", dialogue.dialogue_npc)
            
            # ---------- Continue loop ---------- #
            o = ("Old man: Anything else?", dialogue.dialogue_npc)
            p = ("Yes.", dialogue.dialogue_player)
            q = ("No that should be all.", dialogue.end_dialogue)
            r = ("Old man: What would you like me to go over again?", dialogue.dialogue_npc)


            nodes = [a, b, c, d, e, f, g, h, i, j, k, ka, l, m, ma, n, o, p, q]

            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(nodes)

            dialogue.add_dialogue_edge(a, b)
            dialogue.add_dialogue_edge(a, c)
            dialogue.add_dialogue_edge(a, d)
            dialogue.add_dialogue_edge(a, e)
            dialogue.add_dialogue_edge(a, f)
            dialogue.add_dialogue_edge(a, g)
            dialogue.add_dialogue_edge(a, h)

            dialogue.add_dialogue_edge(b, i)
            dialogue.add_dialogue_edge(c, j)
            dialogue.add_dialogue_edge(d, k)
            dialogue.add_dialogue_edge(k, ka)
            dialogue.add_dialogue_edge(e, l)
            dialogue.add_dialogue_edge(f, m)
            dialogue.add_dialogue_edge(m, ma)
            dialogue.add_dialogue_edge(g, n)

            dialogue.add_dialogue_edge(i, o)
            dialogue.add_dialogue_edge(j, o)
            dialogue.add_dialogue_edge(ka, o)
            dialogue.add_dialogue_edge(l, o)
            dialogue.add_dialogue_edge(ma, o)
            dialogue.add_dialogue_edge(n, o)

            dialogue.add_dialogue_edge(o, p)
            dialogue.add_dialogue_edge(o, q)

            dialogue.add_dialogue_edge(p, r)
            dialogue.add_dialogue_edge(r, b)
            dialogue.add_dialogue_edge(r, c)
            dialogue.add_dialogue_edge(r, c)
            dialogue.add_dialogue_edge(r, e)
            dialogue.add_dialogue_edge(r, f)
            dialogue.add_dialogue_edge(r, g)
            dialogue.add_dialogue_edge(r, h)

            dialogue.run_dialogue()

        def general_store_dialogue_package(*args):
            """Dialogue package for general store trader.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()

            if len(list(args)) == 4:
                special_functions = {"buy_items":args[1], "sell_items":args[1]}
                dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("General store trader: Hello what may I help you with today?", dialogue.dialogue_npc)
            b = ("Nothing.", dialogue.end_dialogue)
            c =  ("I would like to buy items.", dialogue.dialogue_player)
            d =  ("I would like to sell items.", dialogue.dialogue_player)

            e = ("buy_items", dialogue.run_special_function)
            f = ("sell_items", dialogue.run_special_function)

            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(b)
            dialogue.add_dialogue_node(c)
            dialogue.add_dialogue_node(d)
            dialogue.add_dialogue_node(e)
            dialogue.add_dialogue_node(f)

            dialogue.add_dialogue_edge(a, b)
            dialogue.add_dialogue_edge(a, c)
            dialogue.add_dialogue_edge(a, d)
            dialogue.add_dialogue_edge(c, e)
            dialogue.add_dialogue_edge(d, f)

            dialogue.run_dialogue()
        
        def villagers_inn_dialogue_package(*args):
            """Dialogue package for villagers in the inn.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()

            # Dialogue below
                
            a = ("Jacko: I've heard that the dark forest is very dangerous.", dialogue.dialogue_npc)
            b = ("Gruff: Yes old bill went there last night and never came back.", dialogue.dialogue_npc)
            c = ("Jacko: I bet it's those giant spiders. I was telling him but he didn't believe me.", dialogue.dialogue_npc)
            d = ("Gruff: The sheriff is looking for some able bodies to go search for him, you interested?.", dialogue.dialogue_npc)
            e = ("Jacko: Me? No, didn't you just hear me, there's giant spiders.", dialogue.dialogue_npc)

            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(b)
            dialogue.add_dialogue_node(c)
            dialogue.add_dialogue_node(d)
            dialogue.add_dialogue_node(e)
            
            dialogue.add_dialogue_edge(a, b)
            dialogue.add_dialogue_edge(b, c)
            dialogue.add_dialogue_edge(c, d)
            dialogue.add_dialogue_edge(d, e)

            dialogue.run_dialogue()

        if npc_reference == "blacksmith":
            return blacksmith_dialogue_package
        if npc_reference == "oldman":
            return oldman_dialogue_package
        if npc_reference == "oldman_intro":
            return oldman_intro_dialogue_package
        if npc_reference == "villager_ts":
            return villager_ts_dialogue_package
        if npc_reference == "general_store":
            return general_store_dialogue_package
        if npc_reference == "villagers_inn":
            return villagers_inn_dialogue_package
        
    def npc_packages(self, npc_reference):
        """Holds the npc packages.

        Args:
            npc_reference: The npc reference refers to the npc packages to fetch.

        Returns:
            A npc package which is an object.
        """

        blacksmith = SellTrader(self.dialogue_packages(npc_reference="blacksmith"), 
                                "Blacksmith", 
                                products={"1":"Simple copper sword",
                                          "2":"Simple copper chestplate",
                                          "3":"Simple copper helmet",
                                          "4":"Brass ring"}, 
                                item_database=self.item_database,
                                player_reference=self.player_reference)
        
        old_man = Npc(self.dialogue_packages(npc_reference="oldman"), "Old man")
        
        rookie_trainer = Combat(dialogue=None, 
                                name="Rookie Trainer", 
                                base_health=10, 
                                attack=2, 
                                defence=0, 
                                skill_level=1)

        villager_ts = Npc(self.dialogue_packages(npc_reference="villager_ts"), "Villager")

        general_store_trader = SellTrader(self.dialogue_packages(npc_reference="general_store"), 
                                          name="General store trader", 
                                          products={"1":"Health potion",
                                                    "2":"Simple map"}, 
                                        item_database=self.item_database, 
                                        player_reference=self.player_reference)

        villagers_inn = Npc(self.dialogue_packages(npc_reference="vilagers_inn"), "Villagers inn")

        old_man_intro = QuestNPC(self.dialogue_packages(npc_reference="oldman_intro"), "Old man intro", quest_reference=None)

        if npc_reference == "blacksmith":
            return blacksmith
        elif npc_reference == "oldman":
            return old_man
        elif npc_reference == "oldman_intro":
            return old_man_intro
        elif npc_reference == "rookietrainer":
            return rookie_trainer
        elif npc_reference == "villager_ts":
            return villager_ts
        elif npc_reference == "general_store":
            return general_store_trader
        elif npc_reference == "villagers_inn":
            return villagers_inn
        
        
if __name__ == "__main__":
    npcs = WindergardNPCs()

    old_man = npcs.npc_packages("oldman")
    old_man.run_dialogue(dialogue_active=True)


        
    
