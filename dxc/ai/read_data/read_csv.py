import json
import pandas as pd
import urllib.parse #input data
from tkinter import Tk
from tkinter import filedialog
from enum import Enum

def get_file_path_csv():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("csv files", "*.csv")])  
        return file
    file_path = open_file()
    root.destroy()
    return file_path

# try:
#     import google.colab
#     IN_COLAB = True
# except:
#     IN_COLAB = False

# #Read CSV & Excel file from local.
# if IN_COLAB:
    
#     #For CSV file--Google Colab
#     def read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):
#         from google.colab import files
#         uploaded = files.upload()
#         csv_file_name = list(uploaded.keys())[0]
#         df = pd.read_csv(io.BytesIO(uploaded[csv_file_name]), delim_whitespace=delim_whitespace, header = header)
#         if col_names != []:
#             df.columns = col_names
#         return(df)
# else:
#         #For CSV file
#     def read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):
#         csv_path = get_file_path_csv()  
#         df = pd.read_csv(csv_path, delim_whitespace=delim_whitespace, header = header)
#         if col_names != []:
#             df.columns = col_names
#         return(df)


def read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):
    try:
        from google.colab import files
        IN_COLAB = True
    except:
        IN_COLAB = False
    
    if IN_COLAB:
        
        uploaded = files.upload()
        csv_file_name = list(uploaded.keys())[0]
        df = pd.read_csv(io.BytesIO(uploaded[csv_file_name]), delim_whitespace=delim_whitespace, header = header)
        if col_names != []:
            df.columns = col_names
        return(df)
    
    else:     
        csv_path = get_file_path_csv()  
        df = pd.read_csv(csv_path, delim_whitespace=delim_whitespace, header = header)
        if col_names != []:
            df.columns = col_names
        return(df)