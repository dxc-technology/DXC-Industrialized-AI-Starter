import pandas as pd
from tpot import TPOTRegressor
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
from feature_engine import encoding as ce
from .interpret_model import Global_Model_Explanation
from .interpret_model import Explanation_Dashboard
from sklearn import preprocessing
import warnings
import os
import numpy as np
from dxc.ai.global_variables import globals_file
from sklearn.metrics import SCORERS

###encode and return the categorical data
def categorical_encoding(data,target):
    data_1 = data.dropna()
    objFeatures = data_1.select_dtypes(include="object").columns
    objlen = len(list(objFeatures))
    if objlen == 0:             
        return data_1.drop([target], axis = 1), data_1[target]
    else:
        if data_1[target].dtype == 'object':      
            le = preprocessing.LabelEncoder()
            try:
                data_1[target] = le.fit_transform(data_1[target].astype(str))
            except:
                data_1[target] = data_1[target].astype('category')
                data_1[target] = le.fit_transform(data_1[target].astype(str))  
            globals_file.run_experiment_target_encoder = le
            globals_file.run_experiment_target_encoder_used = True
        objFeatures_1 = data_1.select_dtypes(include="object").columns
        objlen_1 = len(list(objFeatures_1))
        if objlen_1 == 0:
            return data_1.drop([target], axis = 1), data_1[target]
        else:
            data_2 = data_1.drop([target], axis = 1)
            encoder = ce.OrdinalEncoder(encoding_method='ordered')
            encoder.fit(data_2, data_1[target])
            data_3 = encoder.transform(data_2)
            globals_file.run_experiment_encoder = encoder
            globals_file.run_experiment_encoder_used = True
            return data_3, data_1[target]

##Define Tpot regressor 
def regressor(verbosity, max_time_mins , max_eval_time_mins, config_dict, warm_start, scoring):
    if verbosity == True:
        model_def = TPOTRegressor(verbosity=2, max_time_mins=max_time_mins, max_eval_time_mins= max_eval_time_mins, config_dict = config_dict, warm_start = warm_start, scoring= scoring, template = 'Regressor')
    else:
        model_def = TPOTRegressor(verbosity=0, max_time_mins=max_time_mins, max_eval_time_mins= max_eval_time_mins, config_dict = config_dict, warm_start = warm_start, scoring= scoring, template = 'Regressor')
    return model_def

##Define Tpot classifier
def classifier(verbosity, max_time_mins, max_eval_time_mins, config_dict, warm_start, scoring):
    if verbosity == True:
        model_def = TPOTClassifier(verbosity=2, max_time_mins=max_time_mins, max_eval_time_mins= max_eval_time_mins, config_dict = config_dict, warm_start = warm_start, scoring = scoring, template = 'Classifier')
    else:
        model_def = TPOTClassifier(verbosity=0, max_time_mins=max_time_mins, max_eval_time_mins= max_eval_time_mins, config_dict = config_dict, warm_start = warm_start, scoring = scoring, template = 'Classifier')
    return model_def

###Train the model 
def train_model(data, target, model_def, model_type, interpret = False, warm_start = False, export_pipeline = True):
    if warm_start == False:
        globals_file.run_experiment_encoder = None
        globals_file.run_experiment_target_encoder = None
        globals_file.run_experiment_target_encoder_used = False
        globals_file.run_experiment_encoder_used = False
        globals_file.run_experiment_warm_start = False
        data_transformed, label_data = categorical_encoding(data,target)
        try:
            x_train, x_test, y_train, y_test = train_test_split(data_transformed, label_data, test_size=0.2, random_state=0, stratify = label_data)
        except:
            x_train, x_test, y_train, y_test = train_test_split(data_transformed, label_data, test_size=0.2, random_state=0) 
    ##Save the data for first time execution with warm start.
    if warm_start == True and globals_file.run_experiment_warm_start == False:
        globals_file.run_experiment_encoder = None
        globals_file.run_experiment_target_encoder = None
        globals_file.run_experiment_target_encoder_used = False
        globals_file.run_experiment_encoder_used = False
        data_transformed, label_data = categorical_encoding(data,target)
        try:
            x_train, x_test, y_train, y_test = train_test_split(data_transformed, label_data, test_size=0.2, random_state=0, stratify = label_data)
        except:
            x_train, x_test, y_train, y_test = train_test_split(data_transformed, label_data, test_size=0.2, random_state=0)
        globals_file.run_experiment_warm_start = True
        globals_file.run_experiment_x_train = x_train
        globals_file.run_experiment_x_test = x_test
        globals_file.run_experiment_y_train = y_train
        globals_file.run_experiment_y_test = y_test
        globals_file.run_experiment_datatransformed = data_transformed
        globals_file.run_experiment_labeldata = label_data
    ##Return the data from second time execution with warm start
    if warm_start == True and globals_file.run_experiment_warm_start == True:
        x_train = globals_file.run_experiment_x_train
        x_test = globals_file.run_experiment_x_test
        y_train = globals_file.run_experiment_y_train
        y_test = globals_file.run_experiment_y_test
        data_transformed = globals_file.run_experiment_datatransformed
        label_data = globals_file.run_experiment_labeldata
    
    model = model_def.fit(x_train, y_train)
    globals_file.run_experiment_model = model
    best_pipeline = model.fitted_pipeline_
    if model_type == 'TPOTRegressor':
        print()
        # r2 score
        score_r2 = SCORERS['r2'](best_pipeline, x_test, y_test)
        print("r2 Score:", score_r2)
        print()
        
        # neg_mean_squared_error
        score_nmse = SCORERS['neg_mean_squared_error'](best_pipeline, x_test, y_test)
        print('Negative mean square error:', score_nmse)
        print()
        
        # neg_root_mean_squared_error
        score_nrmse = SCORERS['neg_root_mean_squared_error'](best_pipeline, x_test, y_test)
        print('Negative root mean square error:', score_nrmse)
        print()
    
        # explained variance
        score_var = SCORERS['explained_variance'](best_pipeline, x_test, y_test)
        print('explained_variance:', score_var)
        print()
    
        # negative mean absolute error
        score_nmae = SCORERS['neg_mean_absolute_error'](best_pipeline, x_test, y_test)
        print('Negative_mean_absolute_error:', score_nmae)
        print()
        
        # Negative median absolute error
        score_nmdae = SCORERS['neg_median_absolute_error'](best_pipeline, x_test, y_test)
        print('Negative_median_absolute_error:', score_nmdae)
        print()
    
    if model_type == 'TPOTClassifier':
        print()   
        # Accuracy 
        score_acc = SCORERS['accuracy'](best_pipeline, x_test, y_test)
        print("Accuracy:", score_acc)
        print()
        
        #ROC_AUC_OVR
        try:
            score_roc_ovr = SCORERS['roc_auc_ovr'](best_pipeline, x_test, y_test)
            print("ROC_AUC_OVR:", score_roc_ovr)
            print()
        except:
            pass
        
        #ROC_AUC_OVO
        try:
            score_roc_ovo = SCORERS['roc_auc_ovo'](best_pipeline, x_test, y_test)
            print("ROC_AUC_OVO:", score_roc_ovo)
            print()
        except:
            pass

        # Recall
        score_rec_macro = SCORERS['recall_macro'](best_pipeline, x_test, y_test)
        print("Recall:", score_rec_macro)        
        print()
        
        # Precision
        score_pre_macro = SCORERS['precision_macro'](best_pipeline, x_test, y_test)
        print("Precision:", score_pre_macro)        
        print()
        
        #F1
        score_f1_macro = SCORERS['f1_macro'](best_pipeline, x_test, y_test)
        print("F1 Score:", score_f1_macro)        
        print()        
        
    
    ##Save the pipeline and data 
    if export_pipeline == True:
        currentDirectory = os.getcwd()
        currentDirectory = currentDirectory + '\data_file.csv'
        data_file_combine = data_transformed
        data_file_combine['target'] = label_data
        data_file_combine.to_csv(currentDirectory, index = False, header=True, encoding='utf-8')
        model.export('best_pipeline.py', currentDirectory)
    ##Generate interpret interactive charts
    if interpret == True:
        global_explanation = Global_Model_Explanation(model.fitted_pipeline_,x_train,x_test,feature_names = None,classes = None,                       explantion_data = None)
        Explanation_Dashboard(global_explanation, model.fitted_pipeline_, x_train, x_test, explantion_data = None)
    return model.fitted_pipeline_
