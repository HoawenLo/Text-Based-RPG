# Contains all item data.

item_database = {}

def return_item_names(item_val):
    """Returns the name of the item from the item_val.
    
    Args:
        item_val: The value of the item.
        
    Returns:
        A string of the item."""
    
    if item_val == None:
        return None

    return item_database[item_val]

item_utils = {"return_item_names": return_item_names}