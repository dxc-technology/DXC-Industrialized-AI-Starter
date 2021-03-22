from interpret_community import TabularExplainer
from raiwidgets import ExplanationDashboard
#from interpret_community.widget import ExplanationDashboard
import warnings

def Global_Model_Explanation(model,x_train,x_test,y_train,y_test,feature_names = None,classes = None, explantion_data = None):
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

def Explanation_Dashboard(global_explanation, model, x_train, x_test, y_train, y_test, explantion_data = None):
    if explantion_data == 'Training':
        ExplanationDashboard(global_explanation, model, dataset=x_train, true_y=y_train)
    else:
        ExplanationDashboard(global_explanation, model, dataset=x_test, true_y=y_test)

    
