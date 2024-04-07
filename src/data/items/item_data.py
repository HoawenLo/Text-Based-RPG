from ..items.item_template import *


# Contains all item data.

# ------------------------ item methods ------------------------ #
class ItemDatabase:

    def __init__(self, character_reference):

        self.character_reference = character_reference

        # --------------- Items --------------- # 

        simple_copper_sword = BasicEquipable(
            item_name="Simple copper sword",
            item_description="A simple copper sword for basic combat needs.",
            item_stack=False,
            value=10,
            attack=4,
            defence=0,
            health=0,
            item_type="Weapon"
        )

        simple_copper_helmet = BasicEquipable(
            item_name="Simple copper helmet",
            item_description="A simple copper helmet for basic combat needs.",
            item_stack=False,
            value=10,
            attack=0,
            defence=2,
            health=0,
            item_type="Helmet"
        )

        simple_copper_chestplate = BasicEquipable(
            item_name="Simple copper chestplate",
            item_description="A simple copper helmet for basic combat needs.",
            item_stack=False,
            value=20,
            attack=0,
            defence=4,
            health=0,
            item_type="Chestplate"
        )

        brass_ring = BasicEquipable(
            item_name="Brass ring",
            item_description="A brass ring. Increases health by 3.",
            item_stack=False,
            value=20,
            attack=0,
            defence=0,
            health=3,
            item_type="Ring"
        )

        apple = EffectItem(
            item_name="Apple",
            item_description="Restores health by 3.",
            item_stack=True,
            value=5,
            passive_effect=None,
            active_effect=self.restore_health_apple,
            item_type="Consumable"
        )


        self.item_database = {
        "Simple copper sword":simple_copper_sword,
        "Simple copper chestplate":simple_copper_chestplate,
        "Simple copper helmet":simple_copper_helmet,
        "Brass ring":brass_ring,
        "Apple": apple
    }
# ------------------------ item special functions ------------------------ #

    def restore_health_apple(self):
        """Restore health by 3.
        
        Args:
            None
            
        Returns:
            None"""    
        
        self.character_reference += 3

# ------------------------ item utility methods ------------------------ #

    def return_item_names(self, item_val):
        """Returns the name of the item from the item_val.
        
        Args:
            item_val: The value of the item.
            
        Returns:
            A string of the item."""
        
        if item_val == None:
            return None

        return self.item_database[item_val]
    






