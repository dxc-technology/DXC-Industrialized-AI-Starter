# from dxc import ai

import pandas as pd

def simple_math():
    x = 2
    y = 3
    try:
        assert x+y == 5
    except:
        print('----------WRONG CALCULATION----------')
    

# loaded_data = None
# raw_data = None
# wrt_raw_data = None
# df = None
# trained_model = None

# def test_load():
#     global loaded_data
#     try:
#         loaded_data = ai.read_data_frame_from_remote_json("https://data.cincinnati-oh.gov/resource/ucjy-ykv4.json")
#         assert type(loaded_data) == type(pd.DataFrame())
#     except:
#         print ('----------INCORRECT URL----------')      

# def test_empty():
#     assert loaded_data.empty == False
    
# text_fields = []
# date_fields = ['date_fleet_doc_entered', 'purchasing_bid_date', 'date_bid_closed', 'date_po_awarded']
# numeric_fields = ['est_unit_cost', 'actual_unit_cost']
# categorical_fields = ['request_id','request_status', 'funding_source', 'request_type', 'department_name', 
#                       'fiscal_year', 'replacement_body_style','equipment_class','equip_id_to_replace',
#                       'replacement_make', 'replacement_model','fleet_document_type', 'procurement_plan']
    
# def test_clean():
#     impute = True
#     global raw_data
#     raw_data = ai.clean_dataframe(loaded_data, impute, text_fields, date_fields, numeric_fields, categorical_fields)
#     assert raw_data.isnull().values.any() == False


# def test_visualize():
#     try:
#         visualize_data = ai.visualize_missing_data(raw_data)
#     except:
#         print('----------VISUALIZATION FAILED----------')

# def test_explore():
#     try:
#         explore_data = ai.explore_features(raw_data)
#     except:
#         print('----------DATA EXPLORATION FAILED----------')
        
# def test_plot():
#     try:
#         plot_data = ai.plot_distributions(raw_data)
#     except:
#         print('----------PLOT DISTRIBUTION FAILED----------')
        

# #data_layer need to be included here for MongoDB access.

# def test_wrt_data():
#     global wrt_raw_data
#     try:
#         wrt_raw_data = ai.write_raw_data(data_layer, raw_data, date_fields)
#     except:
#         print('----------MONGODB CONNECTION FAILED----------')

# def data_pipeline():

#   pipe = [
#           {
#               '$group':{
#                   '_id': {
#                       "funding_source":"$funding_source",
#                       "request_type":"$request_type",
#                       "department_name":"$department_name",
#                       "replacement_body_style":"$replacement_body_style",
#                       "equipment_class":"$equipment_class",
#                       "replacement_make":"$replacement_make",
#                       "replacement_model":"$replacement_model",
#                       "procurement_plan":"$procurement_plan"
#                       },
#                   "avg_est_unit_cost":{"$avg":"$est_unit_cost"},
#                   "avg_est_unit_cost_error":{"$avg":{ "$subtract": [ "$est_unit_cost", "$actual_unit_cost" ] }}
#               }
#           }
#   ]

#   return pipe        

# def test_datepipeline():
#     global df
#     try:
#         df = ai.access_data_from_pipeline(wrt_raw_data, data_pipeline())
#         assert type(df) == type(pd.DataFrame())
#         assert loaded_data.empty == False
#     except:
#         print ('----------ACCESS DATA FROM MONGODB FAILED----------')
        
        
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
