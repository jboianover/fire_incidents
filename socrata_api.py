from config_parser import get_param
from sodapy import Socrata
import pandas as pd

def extract_data():
    #Recovering API parameters
    client_name = get_param('API','client_name')
    file_name = get_param('API','file_name')
    limit_size = get_param('API','limit_size')
    #limit_size = 20000
    client = Socrata(client_name, None)
    try:
        results = client.get(file_name, limit=limit_size)
        #results = client.get_all(file_name)

        df = pd.DataFrame.from_records(results)

        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('sytem', 'system')
        
    except:
        print("Something went wrong while retrieving data.")
    
    return df