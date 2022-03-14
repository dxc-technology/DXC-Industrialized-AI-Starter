from interpret_community import TabularExplainer
from raiwidgets import ExplanationDashboard
#from interpret_community.widget import ExplanationDashboard
import warnings
import sys
from dxc.ai.global_variables import globals_file
import pandas as pd

def get_best_pipeline(github_design): 
    model_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + '/'
    #print(model_path)
    sys.path.insert(1, model_path) 
    #from model_path import best_pipeline
    import best_pipeline
    return best_pipeline.exported_pipeline, best_pipeline.training_features, best_pipeline.testing_features, best_pipeline.training_target, best_pipeline.testing_target

def Global_Model_Explanation(model = None, x_train = pd.DataFrame() , x_test = pd.DataFrame(), y_train = pd.DataFrame(), y_test = pd.DataFrame(), feature_names = None,classes = None, explantion_data = None, design = None):
    warnings.filterwarnings('ignore')
    if globals_file.imported_model_files:
        model, x_train, x_test, y_train, y_test = get_best_pipeline(design)
    if model == None:
        return "Exported Pipeline is missing"
    if x_train.empty:
        return "Training features is missing"
    if x_test.empty:
        return "Testing features is missing"
    if y_train.empty:
        return "Training Target is missing"
    if y_test.empty:
        return "Testing Target is missing"
    #Using SHAP TabularExplainer
    explainer = TabularExplainer(model, 
                                  x_train, 
                                  features=feature_names, 
                                  classes=classes)
    #Generate global explanations
    if explantion_data == 'Training':
        global_explanation = explainer.explain_global(x_train)
    else:
        global_explanation = explainer.explain_global(x_test)
    ##print the global importance rank data
    print('global importance rank: {}'.format(global_explanation.get_feature_importance_dict()))
    #Return Generated Explanation dashboard
    return global_explanation

def Explanation_Dashboard(global_explanation, model = None, x_train = pd.DataFrame() , x_test = pd.DataFrame(), y_train = pd.DataFrame(), y_test = pd.DataFrame(), explantion_data = None, design = None):
    if globals_file.imported_model_files:
        model, x_train, x_test, y_train, y_test = get_best_pipeline(design)
    if model == None:
        return "Exported Pipeline is missing"
    if x_train.empty:
        return "Training features is missing"
    if x_test.empty:
        return "Testing features is missing"
    if y_train.empty:
        return "Training Target is missing"
    if y_test.empty:
        return "Testing Target is missing"

    if explantion_data == 'Training':
        ExplanationDashboard(global_explanation, model, dataset=x_train, true_y=y_train)
    else:
        ExplanationDashboard(global_explanation, model, dataset=x_test, true_y=y_test)
    
