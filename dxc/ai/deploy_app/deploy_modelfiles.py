from git import Repo
from github import Github
import os.path
import git, os, shutil
from dxc.ai.global_variables import globals_file
import pickle
import pandas as pd
from getpass import getpass

def create_git_model_repo(github_design, pat_key):
  gitrepo = Github(pat_key)
  user = gitrepo.get_user()
  git_repo_create = user.create_repo(github_design["Repository_Name"], description= github_design['Project_Description'])
  git_repo_create.create_file(path = "readme.md", message = github_design["Commit_Message"], content = github_design["Project_Description"], branch= github_design["Branch"])
  print("Github Repo %s Created" %github_design["Repository_Name"])

def publish_model_github(github_design, pat_key):    
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

def git_operation_model_clone(DIR_NAME,REMOTE_URL):
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

def git_operation_model_push(DIR_NAME, BRANCH, COMMIT_MSG):
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

def generate_model_files(github_design):
    tpot_data = pd.read_csv('/content\data_file.csv')

    # Save encoder
    
    if globals_file.run_experiment_encoder_used:
        encoder_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/encoder.pkl"
        pickle.dump(globals_file.run_experiment_encoder, open(encoder_save_path, 'wb'))
        print("Data encoder saved in encoder.pkl file")

    # Save dataset
    data_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/prepared_data.csv"
    tpot_data.to_csv(data_save_path, index=False)
    print('Data saved in prepared_data.csv file')

    with open("best_pipeline.py", "r") as txt_file:
        script = txt_file.readlines()
    script = open("best_pipeline.py").read()
    data_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/prepared_data.csv"
    script = script.replace("'/content\\data_file.csv\', sep=\'COLUMN_SEPARATOR\', dtype=np.float64", repr(str(data_save_path)) )
    pipeline_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/best_pipeline.py"
    with open(pipeline_save_path, 'w') as f:
        f.write(script)

    # Save target encoder
    if globals_file.run_experiment_target_encoder_used:
        target_encoder_save_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + "/target_encoder.pkl"
        pickle.dump(globals_file.run_experiment_target_encoder, open(target_encoder_save_path, 'wb'))
        print("Target encoder saved in target_encoder.pkl file")

def publish_model_files(github_design):

    print("Please enter your GitHub PAT")
    pat_key = getpass()

    try:
      create_git_model_repo(github_design, pat_key)
    except:
      print("Github Repo %s already exists" %github_design["Repository_Name"])
    
    DIR_NAME, REMOTE_URL, COMMIT_MSG, BRANCH = publish_model_github(github_design, pat_key)

    git_operation_model_clone(DIR_NAME,REMOTE_URL)

    if not os.path.exists(github_design["Repository_Name"] + '/' + github_design["Github_Model_Folder"]):
       os.makedirs(github_design["Repository_Name"] + '/' + github_design["Github_Model_Folder"]) 

    generate_model_files(github_design)

    git_operation_model_push(DIR_NAME, BRANCH, COMMIT_MSG)
    
    globals_file.imported_model_files = True
    
    os.remove("best_pipeline.py")
