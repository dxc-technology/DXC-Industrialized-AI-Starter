import json
import pandas as pd
import doctest #documenting data stories
import requests #reading data
import datetime
from pymongo import MongoClient #MongoDB
from auto_ml import Predictor #ML models
from sklearn.model_selection import train_test_split
import os
import pickle #serializing models
import Algorithmia
from Algorithmia.errors import AlgorithmException
import shutil #serializing models
import urllib.parse #input data
from git import Git, Repo, remote
from IPython.display import YouTubeVideo
from IPython.core.magic import register_line_cell_magic
import urllib.request, json #input data
from flatten_json import flatten #json input data
import janitor #data cleaning
from ftfy import fix_text #data cleaning
import nltk #data cleaning
nltk.download('punkt') #data cleaning
import scrubadub #data cleaning
import arrow #normalizing dates
import numpy as np
from sklearn.base import TransformerMixin #impute missing data
from sklearn.model_selection import train_test_split #model training
from yellowbrick.features import Rank2D #exploring raw data
import matplotlib.pyplot as plt #exploring raw data
from datacleaner import autoclean #data cleaning
import io #read data from local files
import missingno as msno #gauge dataset completeness
import seaborn as sns #data exploration, distribution plotting
from pandas.api.types import is_numeric_dtype #data exploration, distribution plotting
import math #data exploration, distribution plotting
from tkinter import Tk
from tkinter import filedialog
from enum import Enum
from pandas.io.json import json_normalize
import globals_file

#create an AI guild profile

class AI_Guild_Role(Enum):
    PROJECT_MANAGER = 1,
    DATA_SCIENTIST = 2,
    DATA_ENGINEER = 3,
    ALL = 4

class AI_Badge(Enum):
    CREATE_DATA_STORIES = 1
    RUN_AGILE_TRANSFORMATION = 2
    BUILD_DATA_PIPELINES = 3
    RUN_AI_EXPERIMENT = 4
    BUILD_UTILITY_AI_SERVICES = 5
    PERFORM_AI_FORENSICS = 6
    TEST = 7

guild_role_badges = {
    AI_Guild_Role.PROJECT_MANAGER : [AI_Badge.CREATE_DATA_STORIES, AI_Badge.RUN_AGILE_TRANSFORMATION],
    AI_Guild_Role.DATA_SCIENTIST : [AI_Badge.RUN_AI_EXPERIMENT, AI_Badge.PERFORM_AI_FORENSICS],
    AI_Guild_Role.DATA_ENGINEER : [AI_Badge.BUILD_DATA_PIPELINES, AI_Badge.BUILD_UTILITY_AI_SERVICES],
    AI_Guild_Role.ALL: [AI_Badge.CREATE_DATA_STORIES, AI_Badge.RUN_AGILE_TRANSFORMATION, AI_Badge.BUILD_DATA_PIPELINES, AI_Badge.RUN_AI_EXPERIMENT, AI_Badge.BUILD_UTILITY_AI_SERVICES, AI_Badge.PERFORM_AI_FORENSICS]
}

ai_badge_id = {
    AI_Badge.CREATE_DATA_STORIES: "dd05bbdf-ad5b-469d-ab2c-4dd218fd68fe",
    AI_Badge.RUN_AGILE_TRANSFORMATION: "8ec48861-c355-4e44-b98f-0a80cf1440a8",
    AI_Badge.BUILD_DATA_PIPELINES: "2cffc101-8fc3-4680-a8cd-29ec58483832",
    AI_Badge.RUN_AI_EXPERIMENT: "ddeb2020-1db5-48c6-8b2c-ea2e50f050d7",
    AI_Badge.BUILD_UTILITY_AI_SERVICES: "6e8b661f-31bc-46f7-89e4-194e7e6ebb21",
    AI_Badge.PERFORM_AI_FORENSICS: "ec96e016-9e33-4b4e-a6bd-43491e811179",
    AI_Badge.TEST: "b828e318-8501-434e-9f55-ccdb7000ee09"
}

def guild_member_should_apply_for_badge(guild_member_roles, ai_badge):
    #start by assuming we should not apply for the badge
    apply_for_badge = False
    for role in guild_member_roles:
        #apply for the badge if a matching role is found
        if ai_badge in guild_role_badges[role]: apply_for_badge = True
    return apply_for_badge

def apply_for_an_ai_badge(ai_guild_profile, ai_badge):
    # Construct apiEndponit string
    apiPath = f'badges/{ai_badge_id[ai_badge]}/assertions'
    apiEndpoint = f'{ai_guild_profile["badge_platform_apiHost"]}{ai_guild_profile["badge_platform_apiBasePath"]}{apiPath}'  

    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': ai_guild_profile["badge_platform_apiKey"]
    }

    #for each member in the guild:
    num_guild_members = len(ai_guild_profile['guild_members'])
    for i in range(1,num_guild_members + 1):
    #apply for the badge if applicable
        if guild_member_should_apply_for_badge(ai_guild_profile['guild_members'][i]['roles'], ai_badge):
            payload = {
            'email': ai_guild_profile['guild_members'][i]['badge_applicant_email'],
            'evidence': ai_guild_profile["badge_evidence"]
            }
            response = requests.post(
                apiEndpoint,
                headers=headers,
                json=payload
            )
  
            print(response)
            print(json.dumps(response.json(), indent=4))


#FLATTENING FILE

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
            

class DataFrameImputer(TransformerMixin):
    def __init__(self):
        """Impute missing values.

        Columns of dtype object are imputed with the most frequent value 
        in column.

        Columns of other types are imputed with mean of column.

        """
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

#READING FILE

def get_file_path_csv():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("csv files", "*.csv")])  
        return file
    file_path = open_file()
    root.destroy()
    return file_path

def get_file_path_excel():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("excel files", "*.xlsx")]) 
        return file
    file_path = open_file()
    root.destroy()
    return file_path

def get_file_path_json():
    root = Tk()
    root.update()
    def open_file():
        file = filedialog.askopenfilename(filetypes=[("Json files", "*.json")]) 
        return file
    file_path = open_file()
    root.destroy()
    return file_path

try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

#Read CSV & Excel file from local.
if IN_COLAB:
    
    #For CSV file--Google Colab
    def read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):
        from google.colab import files
        uploaded = files.upload()
        csv_file_name = list(uploaded.keys())[0]
        df = pd.read_csv(io.BytesIO(uploaded[csv_file_name]), delim_whitespace=delim_whitespace, header = header)
        if col_names != []:
            df.columns = col_names
        return(df)
    
    #For Excel file--Google Colab
    def read_data_frame_from_local_excel_file():
        from google.colab import files
        uploaded = files.upload()
        excel_file_name = list(uploaded.keys())[0]
        df = pd.read_excel(io.BytesIO(uploaded[excel_file_name]))
        return(df)
    #For Json file--Google Colab
    def read_data_frame_from_local_json():
        from google.colab import files
        uploaded = files.upload()
        file_name = list(uploaded.keys())[0]
        json_data = json.loads(uploaded[file_name])
        df = flatten_json_into_dataframe(json_data)
        return df
    
else:
    #For CSV file
    def read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):
        csv_path = get_file_path_csv()  
        df = pd.read_csv(csv_path, delim_whitespace=delim_whitespace, header = header)
        if col_names != []:
            df.columns = col_names
        return(df)
    
    #For Excel file
    def read_data_frame_from_local_excel_file():
        excel_path = get_file_path_excel()
        df = pd.read_excel(excel_path)
        return(df)
    
    def read_data_frame_from_local_json():
        json_path = get_file_path_json()
        json_data = json.load(open(json_path))
        df = flatten_json_into_dataframe(json_data)
        return df
    
#Read CSV file from remote.
def read_data_frame_from_remote_csv(csv_url, col_names = [], delim_whitespace=False, header = 'infer'):
    df = pd.read_csv(csv_url, delim_whitespace=delim_whitespace, header = header)
    if col_names != []:
        df.columns = col_names
    return(df)

#Read JSON file from remote
def read_data_frame_from_remote_json(json_url):
    with urllib.request.urlopen(json_url) as url:
        json_data = json.loads(url.read().decode())
    df = flatten_json_into_dataframe(json_data)
    return(df)

#CLEANING FILE

def clean_dataframe(df, impute = False, text_fields = [], date_fields = [], numeric_fields = [], categorical_fields = []):

    clean_df = (
      df
      #make the column names lower case and remove spaces
      .clean_names()

      #remove empty columns
      .remove_empty()

      #remove empty rows and columns
      .dropna(how='all')
    )

    #remove harmful characters. remove personal identifiers. make lowercase
    for field in text_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = clean_df[field].apply(fix_text)
        clean_df[field] = clean_df[field].apply(scrubadub.clean, replace_with='identifier')
        clean_df[field] = clean_df[field].str.lower()
  
    #impute missing values
    if impute:
        clean_df = DataFrameImputer().fit_transform(clean_df)

    #standardize the format of all date fields
    for field in date_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = clean_df[field].apply(arrow.get)

    #make sure all numeric fields have the proper data type
    for field in numeric_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = pd.to_numeric(clean_df[field])
  
    #make sure all categorical variables have the proper data type
    for field in categorical_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = clean_df[field].astype('category')
        
    globals_file.clean_data_used = True

    return(clean_df)

#VISUALIZATION

#display the correlations in pairwise comparisons of all features
def explore_features(df):
    df_copy = df.copy()

    #for some reason, the visualize doesn't accept categorical
    #variables. those have to be converted to strings
    for (col,data) in df_copy.iteritems():
        if df_copy[col].dtype.name == "category":
           df_copy[col] = df_copy[col].astype(str)

    numeric_df = autoclean(df_copy)
    visualizer = Rank2D(algorithm="pearson")
    visualizer.fit_transform(numeric_df)
    visualizer.poof()

#display a visual representation of missing fields in the given data
def visualize_missing_data(df):
    msno.matrix(df, figsize=(15,8))

#plot the distribution of values of each field in the given data
def plot_distributions(df):

    #set plot style
    sns.set(style="darkgrid")

    features = len(df.columns)

    #determine the number of columns in the plot grid and the width and height of each plot
    grid_cols = 3
    plot_width = 5
    plot_height = 3

    #determine the width of the plot grid and number of rows
    grid_width = plot_width * grid_cols
    num_rows = math.ceil(features/grid_cols)

    #determine the width of the plot grid
    grid_height = plot_height * num_rows

    #lay out the plot grid
    fig1 = plt.figure(constrained_layout=True, figsize = (grid_width,grid_height))
    gs = fig1.add_gridspec(ncols = grid_cols, nrows = num_rows)

    #step through the dataframe and add plots for each feature
    current_column = 0
    current_row = 0
    for col in df.columns:

        #set up a plot
        f1_ax1 = fig1.add_subplot(gs[current_row, current_column])
        f1_ax1.set_title(col)

        #create a plot for numeric values
        if is_numeric_dtype(df[col]):
           sns.distplot(df[col], ax = f1_ax1).set_xlabel('')
    
        #creare a plot for categorical values
        if df[col].dtype.name == "category":
           sns.countplot(df[col], ax = f1_ax1, order = df[col].value_counts().index).set_xlabel('')

        #move to the next column
        current_column +=1

        #determine if it is time to start a new row
        if current_column == grid_cols:
           current_column = 0
           current_row +=1

def convert_dates_from_arrow_to_string(df, arrow_date_fields):
    for field in arrow_date_fields:
        df[field] = df[field].apply(format)
    return(df)

def write_raw_data(data_layer, raw_data, arrow_date_fields = []):
    #make the column names lower case and remove spaces
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
    if globals_file.wrt_raw_data_used == True or globals_file.clean_data_used == True:
        pipe = col_header_conv(pipe)
        globals_file.wrt_raw_data_used = False
        globals_file.clean_data_used = False
    data = db.aggregate(pipeline=pipe)
    data = list(data)
    df = json_normalize(data)

    return df

# define the general class of models
class model:
    __model = []
    def build(self, meta_data): raise NotImplementedError()
    def train_and_score(self, data): raise NotImplementedError()
    def interpret(self): raise NotImplementedError()
    def python_object(): raise NotImplementedError()

    @staticmethod
    def meta_data_key(meta_data, value):
        key_list = list(meta_data.keys()) 
        val_list = list(meta_data.values()) 
  
        return key_list[val_list.index(value)] 

#define the model lifecycle
def run_experiment(design):
    design["model"].build(design["meta_data"])
    design["model"].train_and_score(design["data"], design["labels"])
    design["model"].interpret()
    return design["model"].python_object()

# define a prediction model
class prediction(model):

    @property
    def estimator(self):
        raise NotImplementedError()

    def build(self, meta_data):
        self.__model = Predictor(type_of_estimator=self.estimator, column_descriptions=meta_data)
        self.__label = self.meta_data_key(meta_data, "output")

    def train_and_score(self, data, labels):
    # create training and test data
        training_data, test_data = train_test_split(data, test_size=0.2)

    # train the model
        self.__model.train(training_data, verbose=False, ml_for_analytics=False)
  
    # score the model
        self.__model.score(test_data, test_data[self.__label], verbose=0)
  
    def interpret(self):
        pass
  
    def python_object(self):
        return self.__model

# define a regressor model
class regression(prediction):
    @property
    def estimator(self):
        return("regressor")

# define a classification model
class classification(prediction):
    @property
    def estimator(self):
        return("classifier")


def run_experiment(experiment_design):
    # define the general class of models

    experiment_design["model"].build(experiment_design["meta_data"])
    experiment_design["model"].train_and_score(experiment_design["data"], experiment_design["labels"])
    experiment_design["model"].interpret()
      
    return experiment_design["model"].python_object()

   
def publish_microservice(microservice_design, trained_model):
    # create a connection to algorithmia
    client=Algorithmia.client(microservice_design["api_key"])
    api = client.algo(microservice_design["execution_environment_username"] + "/" + microservice_design["microservice_name"])
    
    # create the api if it doesn't exist
    try:
        api.create(
            details = {
                "label": microservice_design['microservice_name'],
            },
            settings = {
                "language": "python3-1",
                "source_visibility": "closed",
                "license": "apl",
                "network_access": "full",
                "pipeline_enabled": True,
                "environment": "cpu"
            }
    )
    except Exception as error:
        print(error)
        
    # create data collection if it doesn't exist
    if not client.dir(microservice_design["model_path"]).exists():
        client.dir(microservice_design["model_path"]).create()
    
    # define a local work directory
    local_dir = microservice_design["microservice_name"]

    # delete local directory if it already exists
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    
    # create local work directory
    os.makedirs(local_dir)

    # serialize the model locally
    local_model = "{}/{}".format(local_dir, "mdl")

    # open a file in a specified location
    file = open(local_model, 'wb')
    # dump information to that file
    pickle.dump(trained_model, file)
    # close the file
    file.close()

    # upload our model file to our data collection
    api_model = "{}/{}".format(microservice_design["model_path"], microservice_design["microservice_name"])
    client.file(api_model).putFile(local_model)

    # encode API key, so we can use it in the git URL
    encoded_api_key = urllib.parse.quote_plus(microservice_design["api_key"])

    algo_repo = "https://{}:{}@git.algorithmia.com/git/{}/{}.git".format(
        microservice_design["execution_environment_username"], 
        encoded_api_key, 
        microservice_design["execution_environment_username"], 
        microservice_design["microservice_name"]
        )

    class Progress(remote.RemoteProgress):
        def line_dropped(self, line):
            print(line)
        def update(self, *args):
            print(self._cur_line)
            
    p = Progress()
    
    try:
        Repo.clone_from(algo_repo, "{}/{}".format(local_dir, microservice_design["microservice_name"]), progress=p)
        cloned_repo = Repo("{}/{}".format(local_dir, microservice_design["microservice_name"]))
    except Exception as error:
        print("here")
        print(error)
        
    api_script_path = "{}/{}/src/{}.py".format(local_dir, microservice_design["microservice_name"], microservice_design["microservice_name"])
    dependency_file_path = "{}/{}/{}".format(local_dir, microservice_design["microservice_name"], "requirements.txt")
        
    # defines the source for the microservice
    results = "{'results':prediction}"
    file_path = "'" + api_model + "'"
    ##Don't change the structure of below docstring
    ##this is the source code needed for the microservice
    src_code_content = """import Algorithmia
import auto_ml
import pandas as pd
import pickle
# create an Algorithmia client
client = Algorithmia.client()
def load_model():
    # Get file by name
    # Open file and load model
\tfile_path = {file_path}
\tmodel_path = client.file(file_path).getFile().name
    # Open file and load model
\twith open(model_path, 'rb') as f:
\t\tmodel = pickle.load(f)
\t\treturn model
trained_model = load_model()
def apply(input):
\tprediction = trained_model.predict(input)
\treturn {results}"""
  
    splitted=src_code_content.split('\n')
    
    ##writes the source into the local, cloned GitHub repository
    with open(api_script_path, "w") as f:
        for line in splitted:
            if line.strip()=="file_path = {file_path}":
                line="\tfile_path = {}".format(file_path)
            if line.strip()=="return {results}":
                line="\treturn {}".format(results)
            f.write(line + '\n')
    
    ##Don't change the structure of below docstring
    ##this is the requirements needed for microservice
    requirements_file_content="""algorithmia>=1.0.0,<2.0
    six
    auto_ml
    pandas
    bottleneck==1.2.1"""
    
    post_split=requirements_file_content.split('\n')
    
    #writes the requirements file into the local, cloned GitHub repository.
    with open(dependency_file_path, "w") as f:
        for line in post_split:
            line = line.lstrip()
            f.write(line + '\n') 
    
    # Publish the microservice
    
    files = ["src/{}.py".format(microservice_design["microservice_name"]), "requirements.txt"]
    cloned_repo.index.add(files)
    cloned_repo.index.commit("Add algorithm files")
    origin = cloned_repo.remote(name='origin')
    
    class Progress(remote.RemoteProgress):
        def line_dropped(self, line):
            print(line)
        def update(self, *args):
            print(self._cur_line)
    
    p = Progress()

    origin.push(progress=p)

    # publish/deploy our algorithm
    client.algo(microservice_design["api_namespace"]).publish()
    
    #  code generates the api endpoint for the newly published microservice
    latest_version = client.algo(microservice_design["api_namespace"]).info().version_info.semantic_version
    api_url = "https://api.algorithmia.com/v1/algo/{}/{}".format(microservice_design["api_namespace"], latest_version)
    
    return api_url
    
