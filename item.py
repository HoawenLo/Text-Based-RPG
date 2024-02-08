class Item:

    def __init__(self, item_name, item_type, item_description, item_stack, item_attack, item_defence, value, passive_effect, active_effect, **class_kwargs):
        self.item_name = item_name
        self.item_type = item_type
        self.item_description = item_description
        self.item_stack = item_stack

        self.attack = item_attack
        self.defence = item_defence
        
        self.value = value

        self.passive_effect = passive_effect
        self.active_effect = active_effect

        self.class_kwargs = class_kwargs

    def execute_passive_effect(self, character, equip_flag):
        if self.passive_effect != None:
            self.passive_effect(character, equip_flag)

    def execute_active_effect(self, character, **external_kwargs):

        if "health_restoration" in self.class_kwargs and self.active_effect != None:
            self.active_effect(character, self.class_kwargs["health_restoration"])

        if "health_restoration" not in self.class_kwargs and self.active_effect != None:
            print("activated")
            self.active_effect(character, external_kwargs)

        

class Object:

    def __init__(self, object_name, items):
        self.object_name = object_name
        self.items = items

simple_copper_sword = Item(item_name="simple copper sword", 
                           item_type="weapon", 
                           item_description="A simple copper sword for basic combat needs.", 
                           item_stack=False,
                           item_attack=3, 
                           item_defence=0,
                           value=10, 
                           passive_effect=None, 
                           active_effect=None)

simple_copper_helmet = Item(item_name="simple copper helmet", 
                            item_type="helmet", 
                            item_description="A simple copper helmet for basic combat needs.", 
                            item_stack=False, 
                            item_attack=0, 
                            item_defence=1,
                            value=10, 
                            passive_effect=None, 
                            active_effect=None)

simple_copper_chestplate = Item(item_name="simple copper chestplate", 
                                item_type="chestplate", 
                                item_description="A simple copper chestplate for basic combat needs.", 
                                item_stack=False, 
                                item_attack=0, 
                                item_defence=3,
                                value=30, 
                                passive_effect=None, 
                                active_effect=None)

def warrior_ring_effect(character, equip_flag):

    print("item effect executed")

    if equip_flag == True:
        print("character has equipped ring")
        if character.attack < 8:
            print("double attack")
            character.attack *= 2
    elif equip_flag == False:
        print("character has unequipped ring")
        character.attack /= 2
    

warrior_ring = Item(item_name="warrior's ring", 
                    item_type="ring", 
                    item_description="A ring which doubles attack if attack is less than 8.", 
                    item_stack=False, 
                    item_attack=0, 
                    item_defence=1, 
                    value=100, 
                    passive_effect=warrior_ring_effect, 
                    active_effect=None)

def restore_health(character, restoration_amount, active=False):

    print("restoratio_amount", restoration_amount)

    health_restored = character.current_health + restoration_amount

    if health_restored > character.base_health:
        character.current_health = character.base_health

    print(f"Current health: {character.current_health}")


simple_health_potion = Item(item_name="simple health potion", 
                            item_type="consumable", 
                            item_description="Restores 5 health.", 
                            item_stack=True, 
                            item_attack=0, 
                            item_defence=0, 
                            value=25, 
                            passive_effect=None, 
                            active_effect=restore_health, 
                            health_restoration=5)

egg = Item(item_name="egg", 
           item_type="quest", 
           item_description="An egg from a chicken.", 
           item_stack=True, 
           item_attack=0, 
           item_defence=0, 
           value=5, 
           passive_effect=None, 
           active_effect=None)

flour = Item(item_name="flour", 
             item_type="quest", 
             item_description="Flour for baking.", 
             item_stack=True, 
             item_attack=0, 
             item_defence=0, 
             value=10, 
             passive_effect=None, 
             active_effect=None)

milk = Item(item_name="milk", 
            item_type="quest", 
            item_description="Some milk.", 
            item_stack=True, 
            item_attack=0, 
            item_defence=0, 
            value=5, 
            passive_effect=None, 
            active_effect=None)

def use_axe(character, kwargs):

    object = kwargs["kwargs"]["object"]

    for reward_item in object.items:
        print(f"You acquired a {reward_item.item_name}")
        character.pickup_item(reward_item)

log = Item(item_name="log", 
           item_type="quest", 
           item_description="Some wood used for crafting.", 
           item_stack=True, 
           item_attack=0,
           item_defence=0, 
           value=0,
           passive_effect=None, 
           active_effect=None)

training_ground_tree = Object(object_name="tree", items=[log])

stone_axe = Item(item_name="stone axe", 
                 item_type="quest", 
                 item_description="A tool used to cut trees or bushes.", 
                 item_stack=False, 
                 item_attack=0, 
                 item_defence=0, 
                 value=10, 
                 passive_effect=None, 
                 active_effect=use_axe)

def show_entire_area(character=None, active=False):
    if active:
        print("Mottengard > Mythos Forest > Astralhaven")


basic_map = Item(item_name="basic map", 
                 item_type="tool", 
                 item_description="A basic map showing the path to Astralhaven", 
                 item_stack=False, 
                 item_attack=0, 
                 item_defence=0, 
                 value=5, 
                 passive_effect=None, 
                 active_effect=show_entire_area)

def beer_output(character=None, active=False):
    if active:
        print("You drink a beer you feel refreshed!")

beer = Item(item_name="beer", 
            item_type="consumable", 
            item_description="A cold beer.", 
            item_stack=True, 
            item_attack=0, 
            item_defence=0, 
            value=5, 
            passive_effect=None, 
            active_effect=beer_output)

apple = Item(item_name="apple", 
             item_type="consumable", 
             item_description="A tasty apple, restores 5 health.", 
             item_stack=True, 
             item_attack=0, 
             item_defence=0, 
             value=5, 
             passive_effect=None, 
             active_effect=restore_health, 
             health_restoration=5)

cake = Item(item_name="cake", 
             item_type="consumable", 
             item_description="A tasty cake, restores 10 health.", 
             item_stack=True, 
             item_attack=0, 
             item_defence=0, 
             value=15, 
             passive_effect=None, 
             active_effect=restore_health, 
             health_restoration=10)

all_items = {"simple copper sword": simple_copper_sword, 
             "simple copper helmet": simple_copper_helmet, 
             "simple copper chestplate":simple_copper_chestplate, 
             "warrior's ring":warrior_ring, 
             "simple health potion":simple_health_potion, 
             "egg":egg, 
             "flour":flour, 
             "milk":milk, 
             "stone axe":stone_axe, 
             "basic map":basic_map, 
             "beer":beer, 
             "apple":apple, 
             "cake":cake}


