from os.path import dirname, join
import csv
import pandas as pd

def load_filedata(module_path, data_file_name):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    try:
        with open(join(module_path, 'data', data_file_name)) as csv_file:
            data_file = csv.reader(csv_file)
            for i, ir in enumerate(data_file):
                if i == 0:
                    header = ir
                    df = pd.DataFrame(columns = header)
                else:
                    df1 = pd.DataFrame([ir],columns = header)
                df = df.append(df1, ignore_index = True)
        return df
    except:
        message = data_file_name[:-4] + " dataset is not available"
        df = pd.DataFrame([message])
        return df


##load data
def load_data(filename):
    module_path = dirname(__file__)
    finalfile = filename + '.csv'
    df = load_filedata(module_path, finalfile)
    return df

#load file content
def load_data_details(filename):
    module_path = dirname(__file__)
    finalfile = filename + '.txt'
    try:
        f = open(join(module_path, 'data', finalfile))
        file_content = f.read()
        return file_content
    except:
        message = "No Details found for " + filename + " data set"
        return message