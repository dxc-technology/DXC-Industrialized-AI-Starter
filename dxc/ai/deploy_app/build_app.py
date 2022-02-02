from git import Repo
from github import Github
import os.path
import git, os, shutil
from dxc.ai.global_variables import globals_file
import pickle
import pandas as pd
from getpass import getpass

def create_git_repo(github_design, pat_key):
  gitrepo = Github(pat_key)
  user = gitrepo.get_user()
  git_repo_create = user.create_repo(github_design["Repository_Name"], description= github_design['Project_Description'])
  git_repo_create.create_file(path = "readme.md", message = github_design["Commit_Message"], content = github_design["Project_Description"], branch= github_design["Branch"])
  print("Github Repo %s Created" %github_design["Repository_Name"])

def publish_github(github_design, pat_key):    
    REMOTE_URL = "https://" + str(pat_key) + "@github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + ".git"
    COMMIT_MSG = github_design["Commit_Message"]
    BRANCH = github_design["Branch"]
    if not os.path.exists(github_design["Repository_Name"]):
      os.makedirs(github_design["Repository_Name"])
      new_path = os.path.join(github_design["Repository_Name"])
      DIR_NAME = new_path
    else:
      DIR_NAME = github_design["Repository_Name"]

    return DIR_NAME, REMOTE_URL, COMMIT_MSG, BRANCH

def publish_model(github_design):

    print("Please enter your GitHub PAT")
    pat_key = getpass()

    try:
      create_git_repo(github_design, pat_key)
    except:
      print("Github Repo %s already exists" %github_design["Repository_Name"])

    DIR_NAME, REMOTE_URL, COMMIT_MSG, BRANCH = publish_github(github_design, pat_key)

    git_operation_clone(DIR_NAME,REMOTE_URL)

    if not os.path.exists(github_design["Repository_Name"] + '/' + github_design["Github_Code_Folder"]):
       os.makedirs(github_design["Repository_Name"] + '/' + github_design["Github_Code_Folder"]) 

    if globals_file.run_experiment_encoder_used:
      encoder_path = "https://github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + "/blob/" + str(github_design["Branch"]) + '/' + str(github_design["Github_Code_Folder"]) + "/encoder.pkl?raw=true"
    else:
      encoder_path = ''
    if globals_file.run_experiment_target_encoder_used:
      target_encoder_path = "https://github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + "/blob/" + str(github_design["Branch"]) + '/' + str(github_design["Github_Code_Folder"]) +"/target_encoder.pkl?raw=true"
    else:
      target_encoder_path = ''
    data_path = "https://raw.githubusercontent.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + '/' + str(github_design["Branch"]) + '/' + str(github_design["Github_Code_Folder"]) + "/prepared_data.csv"

    generate_req_files(github_design)
    generate_app_script(github_design, data_path, encoder_path, target_encoder_path, app_title = github_design["Project_Title"])

    git_operation_push(DIR_NAME, BRANCH, COMMIT_MSG)

def git_operation_clone(DIR_NAME,REMOTE_URL):
  try:
      if os.path.isdir(DIR_NAME):
          shutil.rmtree(DIR_NAME)
      os.mkdir(DIR_NAME)
      repo = git.Repo.init(DIR_NAME)
      origin = repo.create_remote('origin', REMOTE_URL)
      origin.fetch()
      origin.pull(origin.refs[0].remote_head)
  except Exception as e:
      print(str(e))

def git_operation_push(DIR_NAME, BRANCH, COMMIT_MSG):
    try:
        repo = Repo(DIR_NAME)
        try:
          repo.git.checkout('-b', BRANCH)
        except:
          repo.git.checkout(BRANCH)
        repo.git.add('--all')
        repo.index.commit(COMMIT_MSG)
        origin = repo.remote('origin')
        origin.push(BRANCH)
        repo.git.add(update=True)
        print("Github Push Successful")
    except Exception as e:
        print(str(e))

def generate_req_files(github_design):
    tpot_data = pd.read_csv('/content\data_file.csv')

    # Save encoder
    if globals_file.run_experiment_encoder_used:
        encoder_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Code_Folder"]) + "/encoder.pkl"
        pickle.dump(globals_file.run_experiment_encoder, open(encoder_save_path, 'wb'))
        print("Data encoder saved in encoder.pkl file")

    # Save dataset
    data_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Code_Folder"]) + "/prepared_data.csv"
    tpot_data.to_csv(data_save_path, index=False)
    print('Data saved in prepared_data.csv file')

    # Save target encoder
    if globals_file.run_experiment_target_encoder_used:
        target_encoder_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Code_Folder"]) + "/target_encoder.pkl"
        pickle.dump(globals_file.run_experiment_target_encoder, open(target_encoder_save_path, 'wb'))
        print("Target encoder saved in target_encoder.pkl file")


def generate_app_script(github_design, data_path='', encoder_path='', target_encoder_path='', app_title='App deployed by AI-Starter'):    
    requirements = """pip-upgrader
pandas
requests
pickle-mixin
scikit-learn
streamlit
feature-engine"""

    requirement_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Code_Folder"]) + "/requirements.txt"
    with open(requirement_save_path, 'w') as f:
        f.write(requirements)
    print('Generated requirements.txt file')


    with open("best_pipeline.py", "r") as txt_file:
        script = txt_file.readlines()

    script = open("best_pipeline.py").read()
    script = script.replace('import numpy as np', '')
    script = script.replace('import pandas as pd', '')
    script = script.replace("'/content\\data_file.csv\', sep=\'COLUMN_SEPARATOR\', dtype=np.float64", "'prepared_data.csv'")
    script = script.replace("results = exported_pipeline.predict(testing_features)", "")

    #code of app.py
    app_script = """import streamlit as st
import pickle
from io import BytesIO
import requests
import pandas as pd 
# Code from Best Pipeline.py here
best_pipeline
######################
# User defined values
title = 'title of the app'
encoder_location = 'encoder.pkl'
target_encoder_location = 'target_encode.pkl'
if len(encoder_location) > 5:
    mfile = BytesIO(requests.get(encoder_location).content)
    encoder = pickle.load(mfile)
    df = encoder.inverse_transform(features)
else:
    df = features.copy()
if len(target_encoder_location) > 5:
    mfile = BytesIO(requests.get(target_encoder_location).content)
    target_encoder = pickle.load(mfile)
st.title(title)
st.sidebar.header('User Input Parameters')
st.subheader('User Input parameters')
selected_data = dict()
for column in df.columns:
    if column != 'target':
        label = column.replace('_id.','')
        label = label.replace('_',' ').title()
        if df[column].dtype == 'O':
            selected_value = st.sidebar.selectbox(label, list(df[column].unique()))
        elif df[column].dtype == 'int64':
            selected_value = st.sidebar.number_input(label, min_value=df[column].min(), max_value=df[column].max(), value=df[column].iloc[0], step=1)
        elif df[column].dtype == 'float64':
            selected_value = st.sidebar.number_input(label, min_value=df[column].min(), max_value=df[column].max(), value=df[column].iloc[0])
        
        selected_data[column] = selected_value
test_data = pd.DataFrame(selected_data, index=[0])
st.write(test_data)
st.subheader('Prediction')
if len(encoder_location) > 5:
    test_data = encoder.transform(test_data) 
prediction = exported_pipeline.predict(test_data)
if len(target_encoder_location) > 5:
    prediction = target_encoder.inverse_transform(prediction)
if 'float' in str(type(prediction[0])):
    st.write(round(prediction[0],2))
else:
    st.write(prediction[0])
    """

    app_script = app_script.replace('best_pipeline', script)
    app_script = app_script.replace('encoder.pkl', encoder_path)
    app_script = app_script.replace('target_encode.pkl', target_encoder_path)
    app_script = app_script.replace('title of the app', app_title)
    app_script = app_script.replace('prepared_data.csv', data_path)

    app_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Code_Folder"]) + "/app.py"
    with open(app_save_path, 'w') as f:
        f.write(app_script)
    print('Generated app.py file to build the application')
