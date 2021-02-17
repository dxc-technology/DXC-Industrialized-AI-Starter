import json
import pandas as pd
import urllib.parse #input data
from io import BytesIO
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


def read_data_frame_from_local_excel_file(sheet_name=0, header=0, col_names=None, skiprows=None, nrows=None):
    try:
        from google.colab import files
        IN_COLAB = True
    except:
        IN_COLAB = False
        
    if IN_COLAB:
        
        uploaded = files.upload()
        excel_file_name = list(uploaded.keys())[0]
        df = pd.read_excel(BytesIO(uploaded[excel_file_name]),sheet_name=sheet_name, header=header, names=col_names, skiprows=skiprows, nrows=nrows)
        return(df)
    else:
        excel_path = get_file_path_excel()
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header, names=col_names, skiprows=skiprows, nrows=nrows)
        return(df)
    

