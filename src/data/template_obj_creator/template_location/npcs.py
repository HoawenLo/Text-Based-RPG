from ..object_templates.npc_templates import *

class LocationNPCs:

    def __init__(self, item_database):
        self.npc_database = {}
        self.item_databsae = item_database
        self.products = {"1":"item"}

    def dialogue_packages(self, npc_reference):
        """Holds the dialogue packages.

        Args:
            npc_reference: The npc reference refers to the dialogue package to fetch.

        Returns:
            A dialogue package which is a function containing the logic of the dialogue
            to run.
        """

        # Amend variable names to relevant npc
        def npc_dialogue_package(*args):
            """Dialogue package for npc.
            
            Args:
                *args: Accepts any number of arguments as 
                run_dialogue method for NPC varies.

            Returns:
                None
            """

            npc_dialogue = Dialogue()

            # Optional
            if len(list(args)) == 4:
                special_functions = {"special_function":args[1]}
                npc_dialogue.set_special_functions(special_functions)

            # Dialogue below
                
            a = ("NPC: Introduction", npc_dialogue.dialogue_npc)
            b = ((("Nothing.", npc_dialogue.end_dialogue), ("special_function", npc_dialogue.run_special_function), npc_dialogue.show_responses))
            c = ("Nothing.", npc_dialogue.end_dialogue)
            d = ("special_function", npc_dialogue.run_special_function)

            npc_dialogue.initialise_node(a)
            npc_dialogue.add_dialogue_node(b)
            npc_dialogue.add_dialogue_node(c)
            npc_dialogue.add_dialogue_node(d)

            npc_dialogue.add_dialogue_edge(a, b)
            npc_dialogue.add_dialogue_edge(b, c)
            npc_dialogue.add_dialogue_edge(b, d)

            npc_dialogue.run_dialogue()

        if npc_reference == "npc":
            return npc_dialogue_package
        
    def npc_packages(self, npc_reference):
        """Holds the npc packages.

        Args:
            npc_reference: The npc reference refers to the npc packages to fetch.

        Returns:
            A npc package which is an object.
        """

        trader_npc = SellTrader(self.dialogue_packages(npc_reference="npc"), "test_npc", products=self.products, item_database=self.item_database)