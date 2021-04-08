import json
import pandas as pd
import urllib.parse #input data
from tkinter import Tk
from tkinter import filedialog
from enum import Enum
import io

def get_file_path_csv():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("csv files", "*.csv")])  
        return file
    file_path = open_file()
    root.destroy()
    return file_path



def read_data_frame_from_local_csv(col_names = [], sep=',', delim_whitespace=False, header = 'infer', names = None,
                                   skiprows=None, error_bad_lines=True, encoding=None):
    try:
        from google.colab import files
        IN_COLAB = True
    except:
        IN_COLAB = False
    
    if IN_COLAB:
        
        uploaded = files.upload()
        csv_file_name = list(uploaded.keys())[0]
        df = pd.read_csv(io.BytesIO(uploaded[csv_file_name]), sep=sep, delim_whitespace=delim_whitespace, header = header,
                         names=names, skiprows=skiprows, error_bad_lines=error_bad_lines, encoding=encoding)
        if col_names != []:
            df.columns = col_names
        return(df)
    
    else:     
        csv_path = get_file_path_csv()  
        df = pd.read_csv(csv_path, delim_whitespace=delim_whitespace, header = header)
        if col_names != []:
            df.columns = col_names
        return(df)
        
def read_data_frame_from_remote_csv(csv_url, col_names = [], names=None, sep=',',  delim_whitespace=False, header = 'infer', skiprows=None, error_bad_lines=True, encoding=None):
    df = pd.read_csv(csv_url, sep=sep, delim_whitespace=delim_whitespace, header = header, names=names, skiprows=skiprows, error_bad_lines=error_bad_lines, encoding=encoding)
    if col_names != []:
        df.columns = col_names
    return(df)
