from pymongo import MongoClient #MongoDB
import pandas as pd
import json
from dxc.ai.global_variables import globals_file


def convert_dates_from_arrow_to_string(df, arrow_date_fields):
    for field in arrow_date_fields:
        df[field] = df[field].apply(format)
    return(df)

def write_raw_data(data_layer, raw_data, arrow_date_fields = []):
    ##make the column names lower case and remove spaces    
    if globals_file.clean_data_used == True:
        raw_data = raw_data.clean_names()
        globals_file.wrt_raw_data_used = True
        globals_file.clean_data_used = False    
    ##convert your raw data into writable data by converting Arrow dates to strings
    writable_raw_data = convert_dates_from_arrow_to_string(raw_data, arrow_date_fields)
    
    #connect to the data layer
    client = MongoClient(data_layer["connection_string"])
    
    #start a data collection, build a database, insert the raw data
    db = client[data_layer["database_name"]][data_layer["collection_name"]]
    db.insert_many(writable_raw_data.to_dict('records'))
    return db

#Handle case-sensitive for column names in pipeline
def col_header_conv_1(pipe):
    for key,value in pipe.items():
        if type(value) is dict:
            col_header_conv_1(value)
        elif type(value) is list:
            for each in value:
                if type(each) is dict:
                    col_header_conv_1(each)
                else:
                    j = value.index(each)
                    value[j] = '_'.join(each.split()).lower()
        else:
            pipe[key] = '_'.join(value.split()).lower()
    return pipe

def col_header_conv(pipe):
    for i in range(len(pipe)):
        single_pipe = pipe[i]
        new_value = col_header_conv_1(single_pipe)
        pipe[i] = new_value
    return pipe

def access_data_from_pipeline(db, pipe):
    if globals_file.wrt_raw_data_used == True or globals_file.clean_data_used == True:
        pipe = col_header_conv(pipe)
        globals_file.wrt_raw_data_used = False
        globals_file.clean_data_used = False

    data = db.aggregate(pipeline=pipe)
    data = list(data)
    df = pd.io.json.json_normalize(data)
    return df

