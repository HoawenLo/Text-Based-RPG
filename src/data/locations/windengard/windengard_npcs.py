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
                special_functions = {"I would like to buy something.":args[1]}
                dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("Blacksmith: Hello guv how can I help you?", dialogue.dialogue_npc)
            b = ((("Nothing.", dialogue.end_dialogue), ("I would like to buy something.", dialogue.run_special_function), dialogue.show_responses))
            c = ("Nothing.", dialogue.end_dialogue)
            d = ("I would like to buy something.", dialogue.run_special_function)

            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(b)
            dialogue.add_dialogue_node(c)
            dialogue.add_dialogue_node(d)

            dialogue.add_dialogue_edge(a, b)
            dialogue.add_dialogue_edge(b, c)
            dialogue.add_dialogue_edge(b, d)
            dialogue.add_dialogue_edge(d, c)

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


            if len(list(args)) == 4:
                special_functions = {"I would like to buy something.":args[1]}
                blacksmith_dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("Blacksmith: Hello guv how can I help you?", blacksmith_dialogue.dialogue_npc)
            b = ((("Nothing.", blacksmith_dialogue.end_dialogue), ("I would like to buy something.", blacksmith_dialogue.run_special_function), blacksmith_dialogue.show_responses))
            c = ("Nothing.", blacksmith_dialogue.end_dialogue)
            d = ("I would like to buy something.", blacksmith_dialogue.run_special_function)

            blacksmith_dialogue.initialise_node(a)
            blacksmith_dialogue.add_dialogue_node(b)
            blacksmith_dialogue.add_dialogue_node(c)
            blacksmith_dialogue.add_dialogue_node(d)

            blacksmith_dialogue.add_dialogue_edge(a, b)
            blacksmith_dialogue.add_dialogue_edge(b, c)
            blacksmith_dialogue.add_dialogue_edge(b, d)
            blacksmith_dialogue.add_dialogue_edge(d, c)

            blacksmith_dialogue.run_dialogue()



        def oldman_dialogue_package(*args):
            """Dialogue package for oldman. He provides advice on the game.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            dialogue = Dialogue()


            if len(list(args)) == 4:
                special_functions = {"I would like to buy something.":args[1]}
                dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("Old man: Hello how may I be of assistance?", dialogue.dialogue_npc)
            b = ((("Sorry nothing.", dialogue.end_dialogue), 
                  ("Tell me about moving,", dialogue.dialogue_player), 
                  ("Tell me about using the inventory.", dialogue.dialogue_player), 
                  ("Tell me about using the interactions.", dialogue.dialogue_player), 
                  ("Tell me about using the quests.", dialogue.dialogue_player), 
                  ("Tell me about using the stats.", dialogue.dialogue_player), 
                  ("Tell me about using the saving.", dialogue.dialogue_player), 
                  dialogue.show_responses))
            c = ("Sorry nothing.", dialogue.end_dialogue)
            # d = ("Tell me about moving,", dialogue.dialogue_player)
            d = ("To move your character, select the move option (number one), and then relevant location.", dialogue.dialogue_npc)
            e = ("The inventory option (number two) allows you to view your inventory, drop items, equip items and unequip items.", dialogue.dialogue_npc)
            f = ("Available interactions are listed on the player menu. You can select one of them by selecting the interact option. Interactions include talking to NPCs, combat and environment interactions such as cutting trees.", dialogue.dialogue_npc)
            g = ("Select the quests option (number four) to see details for any ongoing or completed quests. This can provide you ideas on what to do next.", dialogue.dialogue_npc)
            h = ("Select the stats option (number five) to see your current stats. Attack increases the amount of damage you can do in combat, whilst defence reduces the damage taken. As you complete quests and win duels you will level up, increasing your base health and attack.", dialogue.dialogue_npc)
            g = ("To save your game select option six. Your game will be saved and you can return at any time!", dialogue.dialogue_npc)
            i = ("Anything else?", dialogue.dialogue_npc)
            j = ((("Yes", dialogue.dialogue_player), 
                  ("No that should be all.", dialogue.end_dialogue),
                  dialogue.show_responses))
            k = ("No that should be all.", dialogue.end_dialogue)


            dialogue.initialise_node(a)
            dialogue.add_dialogue_node(b)
            dialogue.add_dialogue_node(c)
            dialogue.add_dialogue_node(d)

            dialogue.add_dialogue_edge(a, b)
            dialogue.add_dialogue_edge(b, c)
            dialogue.add_dialogue_edge(b, d)
            dialogue.add_dialogue_edge(d, i)
            dialogue.add_dialogue_edge(e, i)
            dialogue.add_dialogue_edge(f, i)
            dialogue.add_dialogue_edge(g, i)
            dialogue.add_dialogue_edge(h, i)
            dialogue.add_dialogue_edge(i, j)
            dialogue.add_dialogue_edge(j, k)
            dialogue.add_dialogue_edge(j, b)

            dialogue.run_dialogue()


        if npc_reference == "blacksmith":
            return blacksmith_dialogue_package
        if npc_reference == "oldman":
            return oldman_dialogue_package
        if npc_reference == "oldman_intro":
            return oldman_intro_dialogue_package
        
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
        
        # old_man_intro = Quest()

        if npc_reference == "blacksmith":
            return blacksmith
        elif npc_reference == "oldman":
            return old_man
        
        
if __name__ == "__main__":
    npcs = WindergardNPCs()

    old_man = npcs.npc_packages("oldman")
    old_man.run_dialogue(dialogue_active=True)


        
    
