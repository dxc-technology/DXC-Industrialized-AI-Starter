import Algorithmia
from Algorithmia.errors import AlgorithmException
import shutil #serializing models
import urllib.parse #input data
from git import Git, Repo, remote
import os
import pickle
from IPython.display import YouTubeVideo
from IPython.core.magic import register_line_cell_magic
import urllib.request, json
from dxc.ai.global_variables import globals_file
from dxc.ai.logging import microservice_logging

def publish_microservice(microservice_design, trained_model, verbose = False):
    #Capture microservice_design in log
    microservice_logging.microservice_design_log(microservice_design)
    # create a connection to algorithmia
    client=Algorithmia.client(microservice_design["api_key"])
    api = client.algo(microservice_design["execution_environment_username"] + "/" + microservice_design["microservice_name"])

    # create the algorithm if it doesn't exist
    try:
        api.create(
            details = {
                "label": microservice_design["microservice_name"],
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
        if verbose == False:
            def line_dropped(self, line):
                pass
            def update(self, *args):
                pass
        else:
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

    ## source code for customized model
    src_code_generalized = """import Algorithmia
import auto_ml
import pandas as pd
import pickle
import json
import numpy as np
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
def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))
def apply(input):
\tprediction = trained_model.predict(input)
\tprediction = json.dumps(prediction, default=default)
\treturn {results}"""

    if globals_file.run_experiment_used:
        src_code_content = src_code_generalized

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
    numpy
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

    p = Progress()

    origin.push(progress=p)

    # publish/deploy our algorithm
    client.algo(microservice_design["api_namespace"]).publish()

    #  code generates the api endpoint for the newly published microservice
    latest_version = client.algo(microservice_design["api_namespace"]).info().version_info.semantic_version
    api_url = "https://api.algorithmia.com/v1/algo/{}/{}".format(microservice_design["api_namespace"], latest_version)

    return api_url
