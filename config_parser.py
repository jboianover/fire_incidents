import os
from pathlib import Path
from configparser import ConfigParser
import ast


def get_param(section, key):
    #use this for jupyter notebook
    #config_file = os.path.join(r'C:\GitHub\fire_incidents', 'config.ini')
    
    #use this for .py script execution
    config_file = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    return config[section][key]
    
def get_dictionary(filename):
    
    #use this for jupyter notebook
    #config_file = os.path.join(r'C:\GitHub\fire_incidents', filename)
    
    #use this for .py script execution
    dictionary_file = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), filename)
    
    #file = open(r'C:\GitHub\fire_incidents\default_dimensions.txt', "r")
    file = open(dictionary_file, "r")

    contents = file.read()
    dictionary = ast.literal_eval(contents)

    return(dictionary)
