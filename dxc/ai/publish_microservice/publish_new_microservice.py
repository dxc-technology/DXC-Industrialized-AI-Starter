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
  git_repo_create = user.create_repo(github_design["Repository_Name"])
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

def publish_app_api(github_design):

    print("Please enter your GitHub PAT")
    pat_key = getpass()

    try:
      create_git_repo(github_design, pat_key)
    except:
      print("Github Repo %s already exists" %github_design["Repository_Name"])

    DIR_NAME, REMOTE_URL, COMMIT_MSG, BRANCH = publish_github(github_design, pat_key)

    git_operation_clone(DIR_NAME,REMOTE_URL)

    if not os.path.exists(github_design["Repository_Name"]):
       os.makedirs(github_design["Repository_Name"]) 

    if globals_file.imported_model_files:

      encoder_file_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/encoder.pkl"
      if os.path.exists(encoder_file_path):
        encoder_path = "https://github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + "/blob/" + str(github_design["Branch"]) + "/encoder.pkl?raw=true"
      else:
        encoder_path = ''
    
      target_encoder_file_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/target_encoder.pkl"
      if os.path.exists(target_encoder_file_path):
        target_encoder_path = "https://github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + "/blob/" + str(github_design["Branch"]) + "/target_encoder.pkl?raw=true"
      else:
        target_encoder_path = ''

      data_path = "https://raw.githubusercontent.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + '/' + str(github_design["Branch"]) + "/prepared_data.csv"
    else:
      if globals_file.run_experiment_encoder_used:
        encoder_path = "https://github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + "/blob/" + str(github_design["Branch"]) + "/encoder.pkl?raw=true"
      else:
        encoder_path = ''
      
      if globals_file.run_experiment_target_encoder_used:
        target_encoder_path = "https://github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + "/blob/" + str(github_design["Branch"]) + "/target_encoder.pkl?raw=true"
      else:
        target_encoder_path = ''
      
      data_path = "https://raw.githubusercontent.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + '/' + str(github_design["Branch"]) + "/prepared_data.csv"

    if globals_file.imported_model_files:
      generate_model_req_files(github_design)
    else:
      generate_req_files(github_design)
    generate_app_script(github_design, data_path, encoder_path, target_encoder_path)

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
        encoder_save_path = str(github_design["Repository_Name"]) + "/encoder.pkl"
        pickle.dump(globals_file.run_experiment_encoder, open(encoder_save_path, 'wb'))
        print("Data encoder saved in encoder.pkl file")

    # Save dataset
    data_save_path = str(github_design["Repository_Name"]) + "/prepared_data.csv"
    tpot_data.to_csv(data_save_path, index=False)
    print('Data saved in prepared_data.csv file')

    # Save target encoder
    if globals_file.run_experiment_target_encoder_used:
        target_encoder_save_path = str(github_design["Repository_Name"]) + "/target_encoder.pkl"
        pickle.dump(globals_file.run_experiment_target_encoder, open(target_encoder_save_path, 'wb'))
        print("Target encoder saved in target_encoder.pkl file")

def generate_model_req_files(github_design):

    data_file_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/prepared_data.csv"
    tpot_data = pd.read_csv(data_file_path)

    # Save encoder
    #if globals_file.run_experiment_encoder_used:
    encoder_file_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/encoder.pkl"
    if os.path.exists(encoder_file_path):
        with open(encoder_file_path, 'rb') as encoder_f:
          encoder_file = pickle.load(encoder_f)
        encoder_save_path = str(github_design["Repository_Name"]) + "/encoder.pkl"
        pickle.dump(encoder_file, open(encoder_save_path, 'wb'))
        print("Data encoder saved in encoder.pkl file")
    
    # Save dataset
    data_save_path = str(github_design["Repository_Name"]) + "/prepared_data.csv"
    tpot_data.to_csv(data_save_path, index=False)
    print('Data saved in prepared_data.csv file')

    # Save target encoder
    target_encoder_file_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/target_encoder.pkl"
    if os.path.exists(target_encoder_file_path):
        with open(target_encoder_file_path, 'rb') as target_f:
          target_encoder = pickle.load(target_f)
        target_encoder_save_path = str(github_design["Repository_Name"]) + "/target_encoder.pkl"
        pickle.dump(target_encoder, open(target_encoder_save_path, 'wb'))
        print("Target encoder saved in target_encoder.pkl file")


def generate_app_script(github_design, data_path='', encoder_path='', target_encoder_path=''):    
    requirements = """pip-upgrader
Flask
pandas
numpy
requests
sklearn
scikit-learn
gunicorn
    """
    
    requirement_save_path = str(github_design["Repository_Name"]) + "/requirements.txt"
    with open(requirement_save_path, 'w') as f:
        f.write(requirements)
    print('Generated requirements.txt file')

    if globals_file.imported_model_files:
      pipeline_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/best_pipeline.py"
      with open(pipeline_save_path, "r") as txt_file:
          script = txt_file.readlines()
      script = open(pipeline_save_path).read()
      git_data_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/prepared_data.csv"
      script = script.replace(git_data_save_path, "prepared_data.csv")
      script = script.replace("results = exported_pipeline.predict(testing_features)", "")
    else:
      with open("best_pipeline.py", "r") as txt_file:
          script = txt_file.readlines()
      script = open("best_pipeline.py").read()
      script = script.replace("'/content\\data_file.csv\', sep=\'COLUMN_SEPARATOR\', dtype=np.float64", "'prepared_data.csv'")
      script = script.replace("results = exported_pipeline.predict(testing_features)", "")

    #code of app.py
    app_script = """import pandas as pd
from flask import Flask, jsonify, request
import pickle
# Code from Best Pipeline.py
best_pipeline
# Flask app script
#app
app = Flask(__name__)
#routes
@app.route('/', methods=['POST'])
def predict():
    #get data
    
    data = request.get_json(force=True)
    
    #convert data into dataframe
    data.update((x, [y]) for x, y in data.items())
    data_df = pd.DataFrame.from_dict(data)
    
    #predictions
    
    try:
      with open('encoder.pkl', 'rb') as f:
          encoder = pickle.load(f)
      data_df = encoder.transform(data_df)
    except:
      print("No encoder exist")
      
    result = exported_pipeline.predict(data_df)
   
    #decode the output
    try:
      with open('target_encoder.pkl', 'rb') as f:
          target_encoder = pickle.load(f)
      result = target_encoder.inverse_transform(result)
    except:
        print("No target encoder exist")
    
    #send back to browser
    output = {'results': result[0]}
    
    #return data
    return jsonify(results=output)
    
if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host ='0.0.0.0', port = 8080, debug = True)
    """
    app_script = app_script.replace('best_pipeline', script)

    app_save_path = str(github_design["Repository_Name"]) + "/app.py"
    with open(app_save_path, 'w') as f:
        f.write(app_script)
    print('Generated app.py file to build the application')

    profile_script = """web: gunicorn app:app"""
    procfile_save_path = str(github_design["Repository_Name"]) + "/Procfile"
    with open(procfile_save_path, 'w') as f:
        f.write(profile_script)
    print('Generated procfile to build the application')  
