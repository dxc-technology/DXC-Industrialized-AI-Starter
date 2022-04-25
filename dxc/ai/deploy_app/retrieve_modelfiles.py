from git import Repo
from github import Github
import os.path
import git, os, shutil
from dxc.ai.global_variables import globals_file
from getpass import getpass

def retrieve_model_files(github_design):
  print("Please enter your GitHub PAT")
  pat_key = getpass()
  REMOTE_URL = "https://" + str(pat_key) + "@github.com/" + str(github_design["GitHub_Username"]) + '/' + str(github_design["Repository_Name"]) + ".git"
  if not os.path.exists(github_design["Repository_Name"]):
    os.makedirs(github_design["Repository_Name"])
    new_path = os.path.join(github_design["Repository_Name"])
    DIR_NAME = new_path
  else:
    DIR_NAME = github_design["Repository_Name"]

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
  globals_file.imported_model_files = True
