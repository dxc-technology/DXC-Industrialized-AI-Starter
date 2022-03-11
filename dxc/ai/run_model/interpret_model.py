from interpret_community import TabularExplainer
from raiwidgets import ExplanationDashboard
#from interpret_community.widget import ExplanationDashboard
import warnings
import sys

model_path = str(github_design["Repository_Name"]) + '/' + str(github_design["Github_Model_Folder"]) + '/'
#print(model_path)
sys.path.insert(1, model_path) 
#from model_path import best_pipeline
import best_pipeline

from best_pipeline import exported_pipeline
from best_pipeline import training_features
from best_pipeline import testing_features
from best_pipeline import training_target
from best_pipeline import testing_target

def Global_Model_Explanation(model = exported_pipeline, x_train = training_features ,x_test = testing_features,y_train = training_target ,y_test = testing_target,feature_names = None,classes = None, explantion_data = None):
    warnings.filterwarnings('ignore')
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

def Explanation_Dashboard(global_explanation, model = exported_pipeline, x_train = training_features , x_test = testing_features, y_train = training_target , y_test = testing_target, explantion_data = None):
    if explantion_data == 'Training':
        ExplanationDashboard(global_explanation, model, dataset=x_train, true_y=y_train)
    else:
        ExplanationDashboard(global_explanation, model, dataset=x_test, true_y=y_test)
    
