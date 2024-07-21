""" IMPORTS """
import configparser
import os
import random

def __read_config(section='', item='') -> None:
    """ 
        Read the Configuration file
        
        Variables: :section:`section`, :item:`item`

        Note:
            * :section:`section` used to define the config.ini section (e.g. [API_KEYS])
            * :item:`item` returns the value of the item you would like.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    # Define the variables to return
    return config[section][item]

def __select_story_file() -> None:
    """
        Select a story file 
    """
    directory = os.listdir(__read_config(section='DEFAULT', item='Stories_path'))
    number_of_files = len(directory)
    # random_number = str(random.randint(1, number_of_files))
    random_number = str(3)
    path = str(__read_config(section='DEFAULT', item='Stories_path'))
    story_file = str( path + 'data_' + random_number + '.json')
    return story_file