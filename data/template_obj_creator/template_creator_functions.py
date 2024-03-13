import numpy as np
import os
import pandas as pd
import pickle
import shutil

# --------------------- Importing Object Data (Location Folders) --------------------- #

def import_object_data(filepath):
    """Import pandas dataframe which stores object data from pickle file.
    This pickle file will be used to populate the 
    
    Args:
        filepath: The filepath to the object csv which contains the parameters."""
    
    with open(filepath, "wb") as file:
        object_data = pickle.load(file)

    return object_data

# --------------------- Creating new object data --------------------- #

def transfer_objects(dir_path, filename, object_data):
    """Transfer created objects to a location directory.
    
    Args:
        dir_path: The directory filepath of the location.
        filename: The filename of object data. Must follow format
        location_object_type.pkl.
        object_data: Object data to export.
        
    Returns:
        None"""

    filepath = os.path.join(dir_path, filename)

    with open(filepath, "wb") as file:
        pickle.dump(object_data, file)

def create_location_folders(location_name):
    """Copies templates for location files and creates a directory of the files.
    
    Args:
        location_name: Name of the location."""
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    locations_filepath = os.path.join(script_directory, "..\locations")

    template_location_filepath = os.path.join(script_directory, "template_location")

    new_location_filepath = os.path.join(locations_filepath, location_name)

    shutil.copytree(template_location_filepath, new_location_filepath)

    for file in os.listdir(new_location_filepath):
        new_filename = location_name + "_" + file
        org_filepath = os.path.join(new_location_filepath, file)
        new_filepath = os.path.join(new_location_filepath, new_filename)
        os.rename(org_filepath, new_filepath)

    print(f"Location folder setup at {new_location_filepath}")

# --------------------- Updating object data --------------------- #

def import_all_pickle_files():
    pass

def update_pickle_files():
    pass

if __name__ == "__main__":
    pass
