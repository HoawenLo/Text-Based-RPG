from ..object_templates.npc_templates import *

class WindergardNPCs:

    def __init__(self, item_database):
        self.npc_database = {}
        self.item_database = item_database

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

            blacksmith_dialogue = Dialogue()

            if len(list(args)) == 4:
                special_functions = {"buy_items":args[1]}
                blacksmith_dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("Blacksmith: Hello guv how can I help you?", blacksmith_dialogue.dialogue_npc)
            b = ((("Nothing.", blacksmith_dialogue.end_dialogue), ("buy_items", blacksmith_dialogue.run_special_function), blacksmith_dialogue.show_responses))
            c = ("Nothing.", blacksmith_dialogue.end_dialogue)
            d = ("buy_items", blacksmith_dialogue.run_special_function)

            blacksmith_dialogue.initialise_node(a)
            blacksmith_dialogue.add_dialogue_node(b)
            blacksmith_dialogue.add_dialogue_node(c)
            blacksmith_dialogue.add_dialogue_node(d)

            blacksmith_dialogue.add_dialogue_edge(a, b)
            blacksmith_dialogue.add_dialogue_edge(b, c)
            blacksmith_dialogue.add_dialogue_edge(b, d)

            blacksmith_dialogue.run_dialogue()

        if npc_reference == "blacksmith":
            return blacksmith_dialogue_package
        
    def npc_packages(self, npc_reference):
        """Holds the npc packages.

        Args:
            npc_reference: The npc reference refers to the npc packages to fetch.

        Returns:
            A npc package which is an object.
        """

        blacksmith = SellTrader(self.dialogue_packages(npc_reference="blacksmith"), 
                                "Blacksmith", 
                                products={"1":"Simple Copper Sword",
                                          "2":"Simple Copper Chestplate",
                                          "3":"Simple Copper Helmet",
                                          "4":"Brass Ring"}, 
                                item_database=self.item_database)
        
        if npc_reference == "blacksmith":
            return blacksmith
        
    
