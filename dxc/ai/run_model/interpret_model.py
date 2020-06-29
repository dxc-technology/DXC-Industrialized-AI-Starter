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
    #Generate Explanation dashboard
    dashboard = ExplanationDashboard(global_explanation, model, datasetX=x_test)
    return dashboard