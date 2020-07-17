from interpret_community import TabularExplainer
from interpret_community.widget import ExplanationDashboard

def Global_Model_Explanation(model,x_train,x_test,feature_names = None,classes = None, explantion_data = None):
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

def Explanation_Dashboard(global_explanation, model, x_train, x_test, explantion_data = None):
    if explantion_data == 'Training':
        ExplanationDashboard(global_explanation, model, datasetX=x_train)
    else:
        ExplanationDashboard(global_explanation, model, datasetX=x_test)

    
