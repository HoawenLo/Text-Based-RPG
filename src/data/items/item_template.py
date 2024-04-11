class Item:
    """Base Item class.
    
    Item classes include:
    
    Base item: Mainly used for stock items.
    EffectItem: Utilised for tools, equippables (inherits) and consumables.
    BasicEquippable: A weapon with no effects.
    SpecialEquippable: A weapon with effects.

    Item types include:
    
    Stock: Item drops that are just used to be sold.
    Tool: Has an active or passive effect for certain use case.
    Weapon: Used for combat, has no effects.
    Helmet: Used for combat, has effect.
    Chestplate: Provides stat boost, has no effects.
    Ring: Provides stat boost, has effects.
    Consumable: Provides temporary stat boost."""
    def __init__(self, item_name, item_description, item_stack, value, item_type="stock"):
        # ----------------- Item Description Properties ----------------- #
        self.item_name = item_name
        self.item_type = item_type
        self.item_description = item_description
        self.item_stack = item_stack

        # ----------------- Value ----------------- #

        self.value = value

class EffectItem(Item):
    """Effect items encompass tool, equippables and consumables."""

    def __init__(self, item_name, item_description, item_stack, value, item_type, passive_effect, active_effect):
        super().__init__(item_name, item_description, item_stack, value, item_type)

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

class BasicEquipable(Item):
    """Encompasses basic equippable - equippables with no effects."""
    def __init__(self, item_name, item_description, item_stack, value, item_type, attack, defence, health):
        super().__init__(item_name, item_description, item_stack, value, item_type)

        self.basic_item = True
        self.attack = attack
        self.defence = defence
        self.health = health

class SpecialEquipable(BasicEquipable, EffectItem):
    """Encompasses special weapons - weapons with effects."""
    def __init__(self, item_name, item_description, item_stack, value, item_type, attack, defence, health, passive_effect, active_effect):
        super(BasicEquipable, self).__init__(item_name, item_description, item_stack, value, item_type, attack, defence, health)
        super(EffectItem, self).__init__(passive_effect, active_effect)

        self.basic_item == False


if __name__ == "__main__":
    # test_item = BasicEquipable(item_name="test",
    #                            item_description="test",
    #                            item_stack=False,
    #                            value=10,
    #                            item_type="Stock",
    #                            attack=1,
    #                            defence=1,
    #                            health=0)


    # if isinstance(test_item.__class__, "__main__.BasicEquipable"):
    #     print("basic equipable")
    pass