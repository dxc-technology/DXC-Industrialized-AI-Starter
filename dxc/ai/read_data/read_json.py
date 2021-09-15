import json
import pandas as pd
import urllib.parse #input data
from flatten_json import flatten
from tkinter import Tk
from tkinter import filedialog
from enum import Enum

def flatten_json_into_dataframe(json_data):
    #flatten the nested JSON data into a data frame
    try:
        json_data_flattened = [flatten(d) for d in json_data]
        df = pd.DataFrame(json_data_flattened)
        return(df)
    except:
        try:
            df = pd.DataFrame(json_data).T
            return(df)
        except:
            raise Exception("Uploaded JSON file is not in proper structure. Please choose different file.")

#Read JSON file from remote
def read_data_frame_from_remote_json(json_url):
    with urllib.request.urlopen(json_url) as url:
        json_data = json.loads(url.read().decode())
    df = flatten_json_into_dataframe(json_data)
    return(df)

def get_file_path_json():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("Json files", "*.json")]) 
        return file
    file_path = open_file()
    root.destroy()
    return file_path


def read_data_frame_from_local_json():
    try:
        from google.colab import files
        IN_COLAB = True
    except:
        IN_COLAB = False
    if IN_COLAB:
        
        uploaded = files.upload()
        file_name = list(uploaded.keys())[0]
        json_data = json.loads(uploaded[file_name])
        df = flatten_json_into_dataframe(json_data)
        return df
    else:
        json_path = get_file_path_json()
        json_data = json.load(open(json_path))
        df = flatten_json_into_dataframe(json_data)
        return df
