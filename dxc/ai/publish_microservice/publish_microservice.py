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
    ##Defining the environment for Algorithmia
    try:
      if microservice_design["environment"].lower() == 'default':
        run_environment = "python38" 
      else:
        run_environment = microservice_design["environment"]
    except:
        run_environment = "python38"
    # create the algorithm if it doesn't exist
    try:
        api.create(
            details = {
                "summary": microservice_design["microservice_description"],
                "label": microservice_design["microservice_name"],
                "tagline": microservice_design["microservice_description"]
            },
            settings = {
                "source_visibility": "closed",
                "package_set": run_environment,
                "license": "apl",
                "network_access": "full",
                "pipeline_enabled": True
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

    if globals_file.run_experiment_encoder_used:
        encode_model = 'encode_file.pkl'
        encode_output = open(encode_model, 'wb')
        pickle.dump(globals_file.run_experiment_encoder, encode_output)
        encode_output.close()
        encode_folder =  microservice_design["microservice_name"] + '_encoder'
        encode_path = "{}/{}".format(microservice_design["model_path"], encode_folder)
        client.file(encode_path).putFile(encode_model)
    if globals_file.run_experiment_target_encoder_used:
        target_encode_model = 'target_encode_file.pkl'
        target_encode_output = open(target_encode_model, 'wb')
        pickle.dump(globals_file.run_experiment_target_encoder, target_encode_output)
        target_encode_output.close()
        target_encode_folder =  microservice_design["microservice_name"] + '_target_encoder'
        target_encode_path = "{}/{}".format(microservice_design["model_path"], target_encode_folder)
        client.file(target_encode_path).putFile(target_encode_model)

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
    if globals_file.run_experiment_encoder_used:
        encodefile_path = "'" + encode_path + "'"
    if globals_file.run_experiment_target_encoder_used:
        target_encodefile_path = "'" + target_encode_path + "'"
    ##Don't change the structure of below docstring
    ##this is the source code needed for the microservice
    
    src_code_content = """import Algorithmia
from Algorithmia import ADK
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
\tprediction = trained_model.predict(pd.DataFrame(input,index = [0]))
\tprediction = json.dumps(prediction, default=default)
\treturn {results}
algorithm = ADK(apply)
algorithm.init("Algorithmia")"""

    ## source code for customized model
    src_code_generalized = """import Algorithmia
from Algorithmia import ADK
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
\tprediction = trained_model.predict(pd.DataFrame(input, index = [0]))
\tprediction = json.dumps(prediction, default=default)
\treturn {results}
algorithm = ADK(apply)
algorithm.init("Algorithmia")"""

    ## source code for generalized tpot model
    src_code_generalized_encode = """import Algorithmia
from Algorithmia import ADK
import pandas as pd
import pickle
import json
import numpy as np
import feature_engine
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
def load_encode():
    # Get file by name
    # Open file and load encoder
\tencodefile_path = {encodefile_path}
\tencode_path = client.file(encodefile_path).getFile().name
    # Open file and load encoder
\twith open(encode_path, 'rb') as f:
\t\tencoder = pickle.load(f)
\t\treturn encoder
encode = load_encode()
def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))
def apply(input):
\tinput = pd.DataFrame([input])
\ttry:
\t\tinput = encode.transform(input)
\texcept:
\t\tpass
\tprediction = trained_model.predict(input)
\tprediction = json.dumps(prediction[0], default=default)
\treturn {results}
algorithm = ADK(apply)
algorithm.init("Algorithmia")"""

    ## source code for generalized tpot model
    src_code_generalized_target_encode = """import Algorithmia
from Algorithmia import ADK
import pandas as pd
import pickle
import json
import numpy as np
import feature_engine
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
def load_target_encode():
    # Get file by name
    # Open file and load target encoder
\ttarget_encodefile_path = {target_encodefile_path}
\ttarget_encode_path = client.file(target_encodefile_path).getFile().name
    # Open file and load target encoder
\twith open(target_encode_path, 'rb') as f:
\t\ttarget_encoder = pickle.load(f)
\t\treturn target_encoder
target_encode = load_target_encode()

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))
def apply(input):
\tinput = pd.DataFrame([input])
\ttry:
\t\tinput = encode.transform(input)
\texcept:
\t\tpass
\tprediction = trained_model.predict(input)
\ttry:
\t\tprediction = target_encode.inverse_transform(prediction)
\t\tprediction = prediction[0]
\texcept:
\t\tprediction = json.dumps(prediction[0], default=default)
\treturn {results}
algorithm = ADK(apply)
algorithm.init("Algorithmia")"""

    ## source code for generalized tpot model
    src_code_generalized_both_encode = """import Algorithmia
from Algorithmia import ADK
import pandas as pd
import pickle
import json
import numpy as np
import feature_engine
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
def load_encode():
    # Get file by name
    # Open file and load encoder
\tencodefile_path = {encodefile_path}
\tencode_path = client.file(encodefile_path).getFile().name
    # Open file and load encoder
\twith open(encode_path, 'rb') as f:
\t\tencoder = pickle.load(f)
\t\treturn encoder
encode = load_encode()
def load_target_encode():
    # Get file by name
    # Open file and load target encoder
\ttarget_encodefile_path = {target_encodefile_path}
\ttarget_encode_path = client.file(target_encodefile_path).getFile().name
    # Open file and load target encoder
\twith open(target_encode_path, 'rb') as f:
\t\ttarget_encoder = pickle.load(f)
\t\treturn target_encoder
target_encode = load_target_encode()

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))
def apply(input):
\tinput = pd.DataFrame([input])
\ttry:
\t\tinput = encode.transform(input)
\texcept:
\t\tpass
\tprediction = trained_model.predict(input)
\ttry:
\t\tprediction = target_encode.inverse_transform(prediction)
\t\tprediction = prediction[0]
\texcept:
\t\tprediction = json.dumps(prediction[0], default=default)
\treturn {results}
algorithm = ADK(apply)
algorithm.init("Algorithmia")"""

    if globals_file.run_experiment_used:
        src_code_content = src_code_generalized
        if globals_file.run_experiment_encoder_used and not globals_file.run_experiment_target_encoder_used:
            src_code_content = src_code_generalized_encode
        if globals_file.run_experiment_target_encoder_used and not globals_file.run_experiment_encoder_used:
            src_code_content = src_code_generalized_target_encode  
        if globals_file.run_experiment_encoder_used and globals_file.run_experiment_target_encoder_used:
            src_code_content = src_code_generalized_both_encode 

    splitted=src_code_content.split('\n')

    ##writes the source into the local, cloned GitHub repository
    with open(api_script_path, "w") as f:
        for line in splitted:
            if line.strip()=="file_path = {file_path}":
                line="\tfile_path = {}".format(file_path)
            if line.strip()=="encodefile_path = {encodefile_path}":
                line="\tencodefile_path = {}".format(encodefile_path)
            if line.strip()=="target_encodefile_path = {target_encodefile_path}":
                line="\ttarget_encodefile_path = {}".format(target_encodefile_path)
            if line.strip()=="return {results}":
                line="\treturn {}".format(results)
            f.write(line + '\n')

    ##Don't change the structure of below docstring
    ##this is the requirements needed for microservice
    requirements_file_content="""algorithmia
    pandas
    numpy
    feature-engine"""

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
    #client.algo(microservice_design["api_namespace"]).publish()
#     api.publish(
#     settings = {
#         "algorithm_callability": "private"
#     },
#     version_info = {
#         "release_notes": "Publishing Microservice",
#         "version_type": "revision"
#     },
#     details = {
#         "label": microservice_design["microservice_name"]
#     }
#     )

    api.publish(
      details = {
        "label": microservice_design["microservice_name"]
      } 
    )

    #  code generates the api endpoint for the newly published microservice
    latest_version = client.algo(microservice_design["api_namespace"]).info().version_info.semantic_version
    api_url = "https://api.algorithmia.com/v1/algo/{}/{}".format(microservice_design["api_namespace"], latest_version)

    return api_url
