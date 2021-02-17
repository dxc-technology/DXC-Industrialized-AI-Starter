# from os.path import dirname, join
# import csv
# import pandas as pd
# 
# def load_filedata(module_path, data_file_name):
#     df = pd.DataFrame()
#     df1 = pd.DataFrame()
#     try:
#         with open(join(module_path, 'data', data_file_name)) as csv_file:
#             data_file = csv.reader(csv_file)
#             for i, ir in enumerate(data_file):
#                 if i == 0:
#                     header = ir
#                     df = pd.DataFrame(columns = header)
#                 else:
#                     df1 = pd.DataFrame([ir],columns = header)
#                 df = df.append(df1, ignore_index = True)
#         return df
#     except:
#         message = data_file_name[:-4] + " dataset is not available"
#         df = pd.DataFrame([message])
#         return df


# ##load data
# def load_data(filename):
#     module_path = dirname(__file__)
#     finalfile = filename + '.csv'
#     df = load_filedata(module_path, finalfile)
#     return df

# #load file content
# def load_data_details(filename):
#     module_path = dirname(__file__)
#     finalfile = filename + '.txt'
#     try:
#         f = open(join(module_path, 'data', finalfile))
#         file_content = f.read()
#         return file_content
#     except:
#         message = "No Details found for " + filename + " data set"
#         return message
    
def load_data(dataset, display_details=False, save_copy=False):

    """
    >>> data = load_data('iris')
    >>> data = load_data('iris', display_details=True)
    >>> data = load_data('iris', display_details=True. save_copy=True)

    """

    import pandas as pd
    import os.path
    import requests
    
    address = "https://raw.githubusercontent.com/dxc-technology/DXC-Industrialized-AI-Starter/master/dxc/ai/datasets/data/"
    extension = ".csv"
    filename = str(dataset) + extension

    complete_address = address + filename

    if os.path.isfile(filename):
        data = pd.read_csv(filename)
    else:
        data = pd.read_csv(complete_address)

    if save_copy:
        save_name = filename
        data.to_csv(save_name, index=False)
    
    if display_details:
        details_extension = ".txt"
        details_filename = str(dataset) + details_extension
        details_complete_address = address + details_filename
        print(requests.get(details_complete_address).text)
    return data



