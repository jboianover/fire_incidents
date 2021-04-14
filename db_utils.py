from config_parser import get_param
import pandas as pd
import mysql.connector
import sqlalchemy

def create_mysql_connection():
    
    #Recovering DB parameters
    hostname = get_param('DB', 'mysql_hostname')
    db_name = get_param('DB', 'db_name')
    user_name= get_param('DB', 'user_name')
    pwd = get_param('DB', 'pwd')

    #Building connection_string
    db_connection_str = 'mysql+mysqlconnector://'+user_name+':'+pwd+'@'+hostname+'/'+db_name
    db_connection = sqlalchemy.create_engine(db_connection_str)
    return db_connection

###########################################################################################

def refresh_db(database_name):
    engine = create_mysql_connection() # connect to server
    engine.execute("DROP DATABASE IF EXISTS " + database_name + ";") #drop db if exists
    engine.execute("CREATE DATABASE " + database_name + ";") #create db
    engine.execute("USE " + database_name + ";") # select new db
    
###########################################################################################    

def read_table_to_df(dim):
    db_connection = create_mysql_connection

    return pd.read_sql('SELECT Id, '+ dim + ' FROM '+ dim, con=db_connection)

###########################################################################################

def load_table(table_name, df, table_action):
    db_connection = create_mysql_connection()
    df.to_sql(name=table_name, con=db_connection, index=False, if_exists=table_action)

    return 0

