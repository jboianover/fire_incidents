import os
from pathlib import Path
from configparser import ConfigParser


def get_param(section, key):
    #use this for jupyter notebook
    #config_file = os.path.join(r'C:\GitHub\fire_incidents', 'config.ini')
    
    #use this for .py script execution
    config_file = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))), 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    return config[section][key]
    