from config_parser import get_param
from sodapy import Socrata
import pandas as pd

def extract_data():
    #Recovering API parameters
    client_name = get_param('API','client_name')
    file_name = get_param('API','file_name')
    limit_size = get_param('API','limit_size')
    
    client = Socrata(client_name, None)
    results = client.get(file_name, limit=limit_size)
    return pd.DataFrame.from_records(results)