import os
from pathlib import Path
from db_utils import refresh_db, read_table_to_df
from socrata_api import extract_data
from data import load_dims, load_fact

def main():

    refresh_db('fire_incidents')
    print("Database refreshed")
    #Extract Data from API
    source_data = extract_data()
    print("Data Extracted: " + str(len(source_data.index)) + " rows in dataset")
    #Create and load Dimensions based on .ini
    load_dims(source_data)
    print('Dimensions Loaded')
    #Create and load Fact Table to DW
    load_fact(source_data, 'fact_fire_incidents')
    print('Fact Table fact_fire_incidents Loaded')
    

if __name__ == "__main__":
    main()