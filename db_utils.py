from config_parser import get_param
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

def create_mysql_connection():
    
    #Recovering DB parameters
    hostname = get_param('DB', 'mysql_hostname')
    db_name = get_param('DB', 'db_name')
    user_name= get_param('DB', 'user_name')
    pwd = get_param('DB', 'pwd')

    #Building connection_string
    db_connection_str = 'mysql+mysqlconnector://'+user_name+':'+pwd+'@'+hostname+'/'+db_name
    db_connection = create_engine(db_connection_str)
    return db_connection

def read_table_to_df(dim):
    db_connection = create_mysql_connection

    return pd.read_sql('SELECT Id, '+ dim + ' FROM '+ dim, con=db_connection)