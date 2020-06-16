import json
import pandas as pd
import urllib.parse #input data
from tkinter import Tk
from tkinter import filedialog
from enum import Enum

def get_file_path_excel():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("excel files", "*.xlsx")]) 
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
#     def read_data_frame_from_local_excel_file():
#         from google.colab import files
#         uploaded = files.upload()
#         excel_file_name = list(uploaded.keys())[0]
#         df = pd.read_excel(io.BytesIO(uploaded[excel_file_name]))
#         return(df)
# else:
#     def read_data_frame_from_local_excel_file():
#         excel_path = get_file_path_excel()
#         df = pd.read_excel(excel_path)
#         return(df)
def read_data_frame_from_local_excel_file():
    try:
        from google.colab import files
        IN_COLAB = True
    except:
        IN_COLAB = False
        
    if IN_COLAB:
        
        uploaded = files.upload()
        excel_file_name = list(uploaded.keys())[0]
        df = pd.read_excel(io.BytesIO(uploaded[excel_file_name]))
        return(df)
    else:
        excel_path = get_file_path_excel()
        df = pd.read_excel(excel_path)
        return(df)
    

