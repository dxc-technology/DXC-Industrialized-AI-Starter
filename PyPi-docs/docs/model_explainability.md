# Model Explainability

In the context of machine learning and artificial intelligence, Explainability is the extent to which the internal mechanics of a machine or deep learning system can be explained in human terms. Model explainability is one of the most important problems in machine learning today.

DXC Industrialized AI Starter helps you to understand the model explainability using interactive dashboards via SHAP - based explainer.

```python
global_explanation = ai.Global_Model_Explanation(model,x_train,x_test,feature_names = None,classes = None, explantion_data = None)
ai.Explanation_Dashboard(global_explanation, model, x_train, x_test, explantion_data = None)
```
To generate the model explainability, you need to pass your model, training data, test data to the functions. You can also optionally pass in feature names and output class names(classification) which will be used to make the explanations and visualizations more informative. Explanations will be generated default on the test data. If you pass the value of explantion_data parameter as 'Training', then the explanation will be generated on training data. But with more examples, explanations will take longer although they may be more accurate.

- __ai.Global_Model_Explanation:__ This function generates the overall model predictions and generates a dictionary of sorted feature importance names and values.

- __ai.Explanation_Dashboard:__  This will generate an interactive visualization dashboard, you can investigate different aspects of your dataset and trained model via below four tab views:

    - Model Performance
    - Data Explorer
    - Aggregate Feature Importance
    - Individual Feature Importance

#### SHAP explainer

SHAP (SHapley Additive exPlanations) is a game theoretic approach to explain the output of any machine learning model. It connects optimal credit allocation with local explanations using the classic Shapley values from game theory and their related extensions. Depending on the model, Model Explainer uses one of the below supported SHAP explainers.

- SHAP TreeExplainer
- SHAP DeepExplainer
- SHAP LinearExplainer
- SHAP KernelExplainer

To know more details about SHAP explainer [click here](https://github.com/slundberg/shap).


Check out [Examples](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/tree/master/Examples) to understand how to use each function, what parameters are expected for each function. Also check out [shap](https://github.com/slundberg/shap), [lime](https://github.com/marcotcr/lime), [interpret-community](https://github.com/interpretml/interpret-community) libraries to learn more about the Model explainability and its usage.

__Note:__ In the present version, Model Explainability supports only the custom models. We are implementing the explainability changes for Auto_ml models. Changes will be published soon.
