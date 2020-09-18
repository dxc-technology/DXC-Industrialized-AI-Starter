from pymongo import MongoClient #MongoDB
import pandas as pd
import json
import datetime
import re
from dxc.ai.global_variables import globals_file
from dxc.ai.logging import pipeline_logging

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
    db_connect = MongoClient(data_layer["connection_string"])
    database=db_connect[data_layer['database_name']]
    collections = database.list_collection_names(include_system_collections=False)
    new_coll=database['meta_data']
    if 'meta_data' not in collections:

        meta_information = { "collection_name": data_layer["collection_name"], "inserted_date_time": datetime.datetime.now(),
                            'data_source':data_layer["data_source"], 'cleaner':data_layer["cleaner"]}
        new_coll.insert_one(meta_information)
        database[data_layer["collection_name"]].insert_many(writable_raw_data.to_dict('records'))
        database["%s_1"%data_layer["collection_name"]].insert_many(writable_raw_data.to_dict('records'))
        meta_information = { "collection_name": "%s_1"%data_layer["collection_name"],  "inserted_date_time": datetime.datetime.now(),
                            'data_source':data_layer["data_source"], 'cleaner':data_layer["cleaner"] }
        new_coll.insert_one(meta_information)

    else:
        if data_layer["collection_name"] in collections:
            tmp = data_layer["collection_name"]
            regex = re.compile(r'%s_\d+'%tmp)
            selected_files = list(filter(regex.search, collections))
            print(selected_files)
            # The list call is only required in Python 3, since filter was changed to return a generator
            length=len(selected_files)
            new_collection="%s_%d"%(data_layer["collection_name"],length+1)
            database[new_collection].insert_many(writable_raw_data.to_dict('records'))
            meta_information = { "collection_name": new_collection,  "inserted_date_time": datetime.datetime.now(),
                            'data_source':data_layer["data_source"], 'cleaner':data_layer["cleaner"] }
            new_coll.insert_one(meta_information)
            database.data_layer["collection_name"].drop()
            new_coll.delete_one({'collection_name':data_layer["collection_name"]})
            database[data_layer["collection_name"]].insert_many(writable_raw_data.to_dict('records'))
            meta_information = { "collection_name": data_layer["collection_name"],  "inserted_date_time": datetime.datetime.now(),
                            'data_source':data_layer["data_source"], 'cleaner':data_layer["cleaner"] }
            new_coll.insert_one(meta_information)
    return database[data_layer["collection_name"]]

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
    df = pd.io.json.json_normalize(data)
    return df
