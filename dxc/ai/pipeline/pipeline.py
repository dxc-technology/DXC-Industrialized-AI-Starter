from pymongo import MongoClient #MongoDB
import pandas as pd
import json
from dxc.ai.global_variables import globals_file
from dxc.ai.logging import pipeline_logging


def convert_dates_from_arrow_to_string(df, arrow_date_fields):
    for field in arrow_date_fields:
        df[field] = df[field].apply(format)
    return(df)

#inserting data into mongo DB
def insert_collection(data_layer, collection_name, df):
  client = MongoClient(data_layer["connection_string"]) #connect to the data layer
  collections = client[data_layer["database_name"]].list_collection_names()
  db = client[data_layer["database_name"]][collection_name]

  #delete the collection if it exists
  if collection_name not in collections:
    db.insert_many(df.to_dict('records'))
  else:
    db.drop()
    db.insert_many(df.to_dict('records'))
  return db

def write_raw_data(data_layer, raw_data, arrow_date_fields = []):
    ##make the column names lower case and remove spaces    
    if globals_file.clean_data_used == True:
        raw_data = raw_data.clean_names()
        globals_file.wrt_raw_data_used = True
        globals_file.clean_data_used = False    
    ##convert your raw data into writable data by converting Arrow dates to strings
    writable_raw_data = convert_dates_from_arrow_to_string(raw_data, arrow_date_fields)
    
    #inserting data into MongoDB collection
    db = insert_collection(data_layer, data_layer["collection_name"], writable_raw_data)
    
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
                    if isinstance(each, str):
                        j = value.index(each)
                        value[j] = '_'.join(each.split()).lower()
        else:
            if isinstance(value, str):
                pipe[key] = '_'.join(value.split()).lower()
    return pipe

def col_header_conv(pipe):
    for i in range(len(pipe)):
        single_pipe = pipe[i]
        new_value = col_header_conv_1(single_pipe)
        pipe[i] = new_value
    return pipe

def access_data_from_pipeline(db, pipe):
    pipeline_logging.pipeline_log(pipe)
    if globals_file.wrt_raw_data_used == True or globals_file.clean_data_used == True:
        pipe = col_header_conv(pipe)
        globals_file.wrt_raw_data_used = False
        globals_file.clean_data_used = False

    data = db.aggregate(pipeline=pipe)
    data = list(data)
    df = pd.json_normalize(data)
    globals_file.run_experiment_warm_start = False
    return df

def store_data_from_pipeline(data_layer, df):
  db = insert_collection(data_layer, data_layer["collection_name"] + '_aggregate', df)
  print('Created data piple line has stored in MongoDB in "%s" collection under "%s" datbase' %(data_layer["collection_name"] + '_aggregate',data_layer["database_name"] ))

