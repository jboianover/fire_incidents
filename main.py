import os
from pathlib import Path
from db_utils import refresh_db
from socrata_api import extract_data
from data import load_dims, load_fact

def main():

    
    refresh_db('fire_incidents')
    #Extract Data from API
    print("Database refreshed")
    source_data = extract_data()
    print("Data Extracted: " + str(len(source_data.index)) + " rows in dataset")
    #Create and load Dimensions based on .ini
    load_dims(source_data)
    print('Dimensions Loaded')
    #Create and load Fact Table to DW
    #load_fact(source_data)

if __name__ == "__main__":
    main()