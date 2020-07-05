from interpret.ext.blackbox import TabularExplainer
from interpret_community.widget import ExplanationDashboard

def interpret_model(model,x_train,x_test,feature_names = None,classes = None):
    #Using SHAP TabularExplainer
    explainer = TabularExplainer(model, 
                                  x_train, 
                                  features=feature_names, 
                                  classes=classes)
    #Generate global explanations
    global_explanation = explainer.explain_global(x_test)
    ##print the global importance rank data
    print('global importance rank: {}'.format(global_explanation.get_feature_importance_dict()))
    #Return Generated Explanation dashboard
    return global_explanation

def Explanation_Dashboard(global_explanation, model, x_train):
    ExplanationDashboard(global_explanation, model, datasetX=x_train)

    
