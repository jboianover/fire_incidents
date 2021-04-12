import os
from pathlib import Path
import db_utils
from socrata_api import extract_data
from data import create_dims, load_fact

def main():

    

    #Extract Data from API
    source_data = extract_data()
    #Create Dimensions based on .ini
    create_dims(source_data)
    #Load Fact Table to DW
    load_fact(source_data)

if __name__ == "__main__":
    main()