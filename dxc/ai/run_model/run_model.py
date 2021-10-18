import arrow #normalizing dates
import numpy as np
from sklearn.base import TransformerMixin #impute missing data
#from auto_ml import Predictor #ML models
from sklearn.model_selection import train_test_split
import os
import pickle
from contextlib import redirect_stdout
import warnings
import io
from dxc.ai.global_variables import globals_file
# from .TimeSeriesModels import getBestForcastingModel
from dxc.ai.logging import experiment_design_logging
from .model_pipeline import regressor
from .model_pipeline import train_model
from .model_pipeline import classifier
from pymongo import MongoClient #MongoDB
import pandas as pd



#Getting data from MongoDB
def get_data_from_pipeline(data_layer):
    #connect to MongoDB
    client = MongoClient(data_layer["connection_string"])
    db = client[data_layer["database_name"]][data_layer["collection_name"] + '_aggregate']
    #getting aggregated pipeline data
    df = pd.json_normalize(list(db.find({},{'_id':0})))
    return df


# define the general class of models
class model:
    __model = []
    def build(self): raise NotImplementedError()
    def train_and_score(self, data): raise NotImplementedError()
    def interpret(self): raise NotImplementedError()
    def python_object(): raise NotImplementedError()

#     @staticmethod
#     def meta_data_key(meta_data, value):
#         key_list = list(meta_data.keys())
#         val_list = list(meta_data.values())

#         return key_list[val_list.index(value)]

#define the model lifecycle


# define a prediction model
class prediction(model):

    @property
    def estimator(self):
        raise NotImplementedError()

    def build(self, target_label, verbose, max_time_mins, max_eval_time_mins, config_dict, warm_start, scoring):
        if self.estimator == 'TPOTRegressor':
            if globals_file.run_experiment_warm_start == False or warm_start == False:
                self.__model = regressor(verbose, max_time_mins, max_eval_time_mins, config_dict, warm_start, scoring)
            else:
                self.__model = globals_file.run_experiment_model
        elif self.estimator == 'TPOTClassifier':
            if globals_file.run_experiment_warm_start == False or warm_start == False:
                self.__model = classifier(verbose, max_time_mins, max_eval_time_mins, config_dict, warm_start, scoring)
            else:
                self.__model = globals_file.run_experiment_model
        else: 
            pass
            #self.__model = Predictor(type_of_estimator=self.estimator, column_descriptions=meta_data)
        self.__label = target_label

    def train_and_score(self, data, labels, verbose, interpret, warm_start, export_pipeline):
        ##Train and score 
        if self.estimator == 'TPOTRegressor' or self.estimator == 'TPOTClassifier':
            self.__model = train_model(data, self.__label, self.__model, self.estimator, interpret, warm_start, export_pipeline)
        else:
            pass
            # create training and test data
            #training_data, test_data = train_test_split(data, test_size=0.2)

        # train the model
            #if verbose == False:
            #    warnings.filterwarnings('ignore')
            #    text_trap = io.StringIO()
            #    with redirect_stdout(text_trap):
            #        self.__model.train(training_data, verbose=False, ml_for_analytics= False)
            #else:
            #    warnings.filterwarnings('ignore')
            #    self.__model.train(training_data, verbose=True, ml_for_analytics=False)

        # score the model
            #if verbose == False:
            #    self.__model.score(test_data, test_data[self.__label], verbose=0)
            #else:
            #    self.__model.score(test_data, test_data[self.__label], verbose=1)

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
    
# define a tpot classification model
class tpot_classification(prediction):
    @property
    def estimator(self):
        return("TPOTClassifier")
    
# define a Tpot regressor model
class tpot_regression(prediction):
    @property
    def estimator(self):
        return("TPOTRegressor")

def run_experiment(design, verbose = False, interpret = False, max_time_mins = 5, max_eval_time_mins = 0.04 , config_dict = None, warm_start = False, export_pipeline = True, scoring = None):
    experiment_design_logging.experiment_design_log(design)
#     if design["model"] == 'timeseries':
#         trained_model = getBestForcastingModel(design['labels'], no_predictions=7, debug=verbose, visualize = False)
#         return trained_model
    globals_file.run_experiment_used = True
    design["model"].build(design["labels"].name, verbose, max_time_mins, max_eval_time_mins, config_dict,warm_start, scoring)
    design["model"].train_and_score(design["data"], design["labels"], verbose, interpret, warm_start, export_pipeline)
    design["model"].interpret()
    return design["model"].python_object()
    
