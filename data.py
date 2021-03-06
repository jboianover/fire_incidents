import pandas as pd
import numpy
from config_parser import get_param, get_dictionary
from db_utils import create_mysql_connection, read_table_to_df, load_table
import ast
import numpy as np
import logging


def load_dims(source_data):

    try:
        load_default_dims(source_data)
    except:
        log = logging.getLogger()
        log.exception("Log Exception Message - Default Dims")
        print("An error occurred while loading default dimensions")

    try:
        load_compound_dims(source_data)
    except:
        log = logging.getLogger()
        log.exception("Log Exception Message - Compound Dims")
        print("An error occurred while loading compound dimensions")

    return 0


def load_default_dims(source_data):
    
    dim_file = get_param('DIM','default')
    default_dim = get_dictionary(dim_file)

    created_dims = []

    for key in default_dim:
        if default_dim[key] in source_data:
            df = dim_by_column(source_data, key, default_dim[key], 0)
            clean_df = df.dropna()
            try:
                load_table('dim_' + key, clean_df, 'replace')
            except:
                print("An error occurred while loading default dimension " + key)
            created_dims.append(key)
        else:
            raise Exception("ERROR: The column "+ default_dim[key] + " does not exist - Verify and correct " + dim_file)

    if len(default_dim) != len(created_dims):
        raise Exception("ERROR: there were some dimensions that couldn't been created - \n \
            Dimension List: "+ ','.join(list(default_dim.keys()))+ "\nCreated Dimensions" \
                + ','.join(created_dims))
    else:
        print("Default dims created: " + ', '.join(created_dims))
        return created_dims     

######################################################################################################################################

def load_compound_dims(source_data):
    
    dim_file = get_param('DIM','compound')
    compound_dim = get_dictionary(dim_file)

    created_dims = []

    for key in compound_dim:
        i = 1
        for column_name in compound_dim[key]:
            if column_name in source_data:
                if i == 1:
                    df_acum = dim_by_column(source_data, key, column_name, 0)
                else:
                    base_id = len(df_acum.index)
                    df_acum = pd.concat([df_acum, dim_by_column(source_data, key, column_name, base_id)], ignore_index=True)
                    new_column_name = key + '_desc'
                    df_acum = df_acum[new_column_name].drop_duplicates(inplace=False).sort_values().reset_index(drop=True).dropna().to_frame()
                i += 1
            else:
                raise Exception("ERROR: The column "+ column_name + " does not exist - Verify and correct " + dim_file)
        clean_df = df_acum.dropna()
        clean_df['Id'] = clean_df.index + 1
        column_list = ['Id', new_column_name]
        final_df = clean_df[column_list]
        load_table('dim_' + key, final_df, 'replace')
        created_dims.append(key)

    if len(compound_dim) != len(created_dims):
        raise Exception("ERROR: there were some dimensions that couldn't been created - \n \
            Dimension List: "+ ','.join(list(compound_dim.keys()))+ "\nCreated Dimensions" \
                + ','.join(created_dims))
    else:
        print("Compound dims created: " + ', '.join(created_dims))
        return created_dims

######################################################################################################################################

def dim_by_column(df, dim_name, column_name, base_id):
    
    #This function returns a pandas dataframe with a sequential autogenerated Id and the attribute to be dimensioned
    clean_df = df[column_name].drop_duplicates(inplace=False).sort_values().reset_index(drop=True).dropna().to_frame()
    clean_df['Id'] = clean_df.index + base_id + 1
    dim_df = clean_df[['Id',column_name]]
    final_df = dim_df.rename(columns = {column_name: dim_name + '_desc'}, inplace = False)
    return final_df

#######################################################################################################################################

def lookup_default_dim(df):
    
    dim_file = get_param('DIM','default')
    default_dim = get_dictionary(dim_file)

    replaced_dims = []
    i = 1
    for key in default_dim:
        
        if default_dim[key] in df:
            table_name = "dim_" + key
            dim_df = read_table_to_df(table_name)
            if i == 1:
                replaced_df = replace_attrib_for_id(df, dim_df, default_dim[key], key + "_desc")
            else:
                replaced_df = replace_attrib_for_id(replaced_df, dim_df, default_dim[key], key + "_desc")
            replaced_dims.append(key)
        else:
            raise Exception("ERROR: The column "+ default_dim[key] + " does not exist - Verify and correct " + dim_file)
        i +=1
    if len(default_dim) != len(replaced_dims):
        raise Exception("ERROR: there were some dimensions that couldn't been created - \n \
            Dimension List: "+ ','.join(list(default_dim.keys()))+ "\nCreated Dimensions" \
                + ','.join(replaced_dims))
    
    return replaced_df

#######################################################################################################################################

def lookup_compound_dim(df):
    
    dim_file = get_param('DIM','compound')
    compound_dim = get_dictionary(dim_file)

    replaced_dims = []
    i = 1
    for key in compound_dim:
        table_name = "dim_" + key
        dim_df = read_table_to_df(table_name)
        j = 1    
        for column_name in compound_dim[key]:
            if column_name in df:
                if i == 1 and j == 1:
                    replaced_df = replace_attrib_for_id(df, dim_df, column_name, key + "_desc")
                else:
                    replaced_df = replace_attrib_for_id(replaced_df, dim_df, column_name, key + "_desc")
                j += 1        
            else:
                raise Exception("ERROR: The column "+ column_name + " does not exist - Verify and correct " + dim_file)
        replaced_dims.append(key)
        i += 1
    if len(compound_dim) != len(replaced_dims):
        raise Exception("ERROR: there were some dimensions that couldn't been created - \n \
                Dimension List: "+ ','.join(list(compound_dim.keys()))+ "\nCreated Dimensions: " \
                    + ','.join(replaced_dims))
    
    return replaced_df

######################################################################################################################################

def replace_attrib_for_id(source_df, dim_df, column_name, dim_column):
    
    joined_df = pd.merge(source_df, dim_df, left_on = column_name, right_on = dim_column, how='left')
    joined_df = joined_df.drop(columns=[column_name])
    joined_df[column_name] = joined_df['Id']
    replaced_df = joined_df.drop(columns=['Id'])
    replaced_df = replaced_df.drop(columns=[dim_column])

    return replaced_df

######################################################################################################################################

def load_fact(df, table_name):
    
    try:
        fact_df = lookup_default_dim(df)
        fact_df = lookup_compound_dim(fact_df)
        fact_df['incident_number'] = fact_df['incident_number'].astype(int)
        fact_df['id'] = fact_df['id'].astype(int)
        fact_df['incident_date']= pd.to_datetime(fact_df['incident_date'])
        fact_df['alarm_dttm']= pd.to_datetime(fact_df['alarm_dttm'])
        fact_df['arrival_dttm']= pd.to_datetime(fact_df['arrival_dttm'])
        fact_df['close_dttm']= pd.to_datetime(fact_df['close_dttm'])
        fact_df['point'] = fact_df['point'].astype(str)
        load_table(table_name, fact_df, 'replace')

    except:
        log = logging.getLogger()
        log.exception("Log Exception Message - Default Dims")
        print("An error occurred while loading fact table")

    return 0