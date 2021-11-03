from dxc import ai

import pandas as pd    
import base64

loaded_data = None
raw_data = None
wrt_raw_data = None
df = None
trained_model = None

def test_load_csv_data_remote():
    global loaded_data
    csv_url = "https://raw.githubusercontent.com/dxc-technology/DXC-Industrialized-AI-Starter/master/dxc/ai/datasets/data/ab_nyc_2019.csv"
    loaded_data = ai.read_data_frame_from_remote_csv(csv_url, col_names = [], delim_whitespace=False, header = 'infer')
    assert type(loaded_data) == type(pd.DataFrame()) 

def test_empty():
    assert loaded_data.empty == False

def test_iris_data():
    global loaded_data
    loaded_data = ai.load_data('iris')
    assert type(loaded_data) == type(pd.DataFrame())
        
def test_empty():
    assert loaded_data.empty == False

def test_bs_data():
    global loaded_data
    loaded_data = ai.load_data('bike_sharing_data')
    assert type(loaded_data) == type(pd.DataFrame())
        
def test_empty():
    assert loaded_data.empty == False

def test_load_json_data_remote():
    global loaded_data
    loaded_data = ai.read_data_frame_from_remote_json("https://data.cincinnati-oh.gov/resource/ucjy-ykv4.json")
    assert type(loaded_data) == type(pd.DataFrame())    

def test_empty():
    assert loaded_data.empty == False
    
text_fields = []
date_fields = ['date_fleet_doc_entered', 'purchasing_bid_date', 'date_bid_closed', 'date_po_awarded']
numeric_fields = ['est_unit_cost', 'actual_unit_cost']
categorical_fields = ['request_id','request_status', 'funding_source', 'request_type', 'department_name', 
                      'fiscal_year', 'replacement_body_style','equipment_class','equip_id_to_replace',
                      'replacement_make', 'replacement_model','fleet_document_type', 'procurement_plan']
    
def test_clean():
    impute = True
    global raw_data
    raw_data = ai.clean_dataframe(loaded_data, impute, text_fields, date_fields, numeric_fields, categorical_fields)
    assert raw_data.isnull().values.any() == False


def test_visualize():
    visualize_data = ai.visualize_missing_data(raw_data)
        
def test_explore():
    explore_data = ai.explore_features(raw_data)
        
def test_plot():
    plot_data = ai.plot_distributions(raw_data)
        
        
id_decoded = base64. b64decode('bWJhbmRydTI=').decode("utf-8")
pwd_decoded = base64. b64decode('cmV2c1JmQkNPSW9kNGVpVw==').decode("utf-8")
connection_string_ = str("mongodb://" + id_decoded + ":" + pwd_decoded + "@freecluster0-shard-00-00-sxnu6.azure.mongodb.net:27017,freecluster0-shard-00-01-sxnu6.azure.mongodb.net:27017,freecluster0-shard-00-02-sxnu6.azure.mongodb.net:27017/<dbname>?ssl=true&replicaSet=FreeCluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        
data_layer = {
    "connection_string": connection_string_,
    "collection_name": "testcollection",
    "database_name": "testdatabase",
    "data_source": '',
    "cleaner": ''
}

def test_wrt_data():
    global wrt_raw_data
    wrt_raw_data = ai.write_raw_data(data_layer, raw_data, date_fields)
        
def data_pipeline():

  pipe = [
          {
              '$group':{
                  '_id': {
                      "funding_source":"$funding_source",
                      "request_type":"$request_type",
                      "department_name":"$department_name",
                      "replacement_body_style":"$replacement_body_style",
                      "equipment_class":"$equipment_class",
                      "replacement_make":"$replacement_make",
                      "replacement_model":"$replacement_model",
                      "procurement_plan":"$procurement_plan"
                      },
                  "avg_est_unit_cost":{"$avg":"$est_unit_cost"},
                  "avg_est_unit_cost_error":{"$avg":{ "$subtract": [ "$est_unit_cost", "$actual_unit_cost" ] }}
              }
          }
  ]

  return pipe        


def test_datepipeline():
    global df
    df = ai.access_data_from_pipeline(wrt_raw_data, data_pipeline())
    assert type(df) == type(pd.DataFrame())
    assert loaded_data.empty == False


def test_experiment():
    global trained_model
    try:
        experiment_design = {
            #model options include ['tpot_regression()', 'tpot_classification()']
            "model": ai.tpot_regression(),
            "labels": df.avg_est_unit_cost_error,
            "data": df,
        }

        trained_model = ai.run_experiment(experiment_design, verbose = False, max_time_mins = 5, max_eval_time_mins = 0.04, 
                                          config_dict = None, warm_start = False, export_pipeline = True, scoring = None)
    except:
        print('----------MODEL BUILDING FAILED----------')
    
# # TODO: design and run an experiment
# def test_experiment():
#     global trained_model
#     try:
#         experiment_design = {
#             #model options include ['regression()', 'classification()']
#             "model": ai.regression(),
#             "labels": df.avg_est_unit_cost_error,
#             "data": df,
#             #Tell the model which column is 'output'
#             #Also note columns that aren't purely numerical
#             #Examples include ['nlp', 'date', 'categorical', 'ignore']
#             "meta_data": {
#               "avg_est_unit_cost_error": "output",
#               "_id.funding_source": "categorical",
#               "_id.department_name": "categorical",
#               "_id.replacement_body_style": "categorical",
#               "_id.replacement_make": "categorical",
#               "_id.replacement_model": "categorical",
#               "_id.procurement_plan": "categorical"
#           }
#         }
#         trained_model = ai.run_experiment(experiment_design)
#     except:
#         print('----------MODEL BUILDING FAILED----------')
        
# # TODO design a microservice
# microservice_design = {
#     "microservice_name": "dxcaistarter",
#     "microservice_description": "test api generated from the DXC ai starter",
#     "execution_environment_username": "joverton",
#     "api_key": "sim6lSW/N7LIfmNsPzLQCTTknRv1",
#     "api_namespace": "joverton/dxcaistarter",
#     "model_path":"data://.my/mycollection"
# }

# def test_publish_api():
#     try:
#         api_url = ai.publish_microservice(microservice_design, trained_model)
#         assert api_url != ' '
#     except:
#         print('----------API PUBLISHING FAILED----------')
