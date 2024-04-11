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

        health_potion = EffectItem(
            item_name="Health potion",
            item_description="Restores health by 10.",
            item_stack=True,
            value=15,
            passive_effect=None,
            active_effect=self.restore_health_potion,
            item_type="Consumable"
        )

        simple_map = EffectItem(
            item_name="Simple map",
            item_description="Displays the major areas of the world.",
            item_stack=False,
            value=3,
            passive_effect=None,
            active_effect=self.simple_map,
            item_type="Tool"
        )

        self.item_database = {
        "Simple copper sword":simple_copper_sword,
        "Simple copper chestplate":simple_copper_chestplate,
        "Simple copper helmet":simple_copper_helmet,
        "Brass ring":brass_ring,
        "Apple": apple,
        "Health potion":health_potion,
        "Simple map":simple_map
    }
# ------------------------ item special functions ------------------------ #

    def restore_health_apple(self, character_reference):
        """Restore health by 3.
        
        Args:
            None
            
        Returns:
            None"""    
        
        self.character_reference.current_health += 3
        print("Health restored by 3 points")
        if self.character_reference.current_health > self.character_reference.base_health:
            self.character_reference.current_health = self.character_reference.base_health
    
    def restore_health_potion(self, character_reference):
        """Restore health by 10.
        
        Args:
            None
            
        Returns:
            None"""    
        
        self.character_reference.current_health += 10
        print("Health restored by 10 points")
        if self.character_reference.current_health > self.character_reference.base_health:
            self.character_reference.current_health = self.character_reference.base_health

    def simple_map(self):
        """Prints a simple map of the world."""

        print("Windengard -- Dark Forest -- Astralhaven")

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
    






