class Item:
    """Base Item class.
    
    Item types include:
    
    Stock: Item drops that are just used to be sold.
    Tool: Has an active or passive effect for certain use case.
    Basic Weapon: Used for combat, has no effects.
    Special Weapon: Used for combat, has effect.
    Basic Equippable: Provides stat boost, has no effects.
    Special Equippable: Provides stat boost, has effects.
    Consumable: Provides temporary stat boost."""
    def __init__(self, item_name, item_description, item_stack, value):
        # ----------------- Item Description Properties ----------------- #
        self.item_name = item_name
        self.item_type = "stock"
        self.item_description = item_description
        self.item_stack = item_stack

        # ----------------- Value ----------------- #

        self.value = value

class EffectItem(Item):
    """Effect items encompass tool, equippables and consumables."""

    def __init__(self, item_name, item_description, item_stack, value, passive_effect, active_effect):
        super().__init__(item_name, item_description, item_stack, value)

    # ----------------- Item Description Properties ----------------- #

        self.item_type = "effect_item"

    # ----------------- Effects ----------------- #

        self.passive_effect = passive_effect
        self.active_effect = active_effect     

    def execute_passive_effect(self, player):
        """Execute passive effect when equipped.
        
        Args:
            player: Reference to player object."""
        
        if self.passive_effect != None:
            self.passive_effect(player)

    def execute_active_effect(self, player):
        """Execute passive effect when equipped.
        
        Args:
            player: Reference to player object."""
        
        if self.active_effect != None:
            self.active_effect(player)

class BasicWeapon(Item):
    """Encompasses basic weapons - weapons with no effects."""
    def __init__(self, item_name, item_description, item_stack, value, attack, defence, health):
        super().__init__(item_name, item_description, item_stack, value)

        self.attack = attack
        self.defence = defence
        self.health = health
        self.item_type = "weapon"

class SpecialWeapon(BasicWeapon, EffectItem):
    """Encompasses special weapons - weapons with effects."""
    def __init__(self, item_name, item_description, item_stack, value, attack, defence, health):
        super(BasicWeapon, self).__init__(item_name, item_description, item_stack, value, attack, defence, health)
        super(EffectItem, self).__init__(attack, defence)

class BasicArmour(Item):
    """Encompasses basic armour pieces - armour with no effects."""
    def __init__(self, item_name, item_description, item_stack, value, attack, defence, health):
        super().__init__(item_name, item_description, item_stack, value)

        self.attack = attack
        self.defence = defence
        self.health = health
        self.armour = "armour"

class SpecialArmour(BasicWeapon, EffectItem):
    """Encompasses special armour pieces - armour pieces with effects."""
    def __init__(self, item_name, item_description, item_stack, value, attack, defence, health):
        super(BasicArmour, self).__init__(item_name, item_description, item_stack, value, attack, defence, health)
        super(EffectItem, self).__init__(attack, defence)

        