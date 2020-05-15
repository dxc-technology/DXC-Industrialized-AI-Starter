# Run AI Experiments
---
An experiment trains and tests a machine-learning model. The code in this section runs a model through a complete lifecycle and saves the final model to the local drive. Run the code that defines a machine-learning model and its lifecycle. Design an experiment and execute it. Most of the work of choosing features and specific model parameters will be done automatically. The code will also automatically score each option and return the options with the best predictive performance.

Below is a example for run_experiment() function.
```
experiment_design = {
    #model options include ['regression()', 'classification()']
    "model": ai.regression(),
    "labels": df.avg_est_unit_cost_error,
    "data": df,
    #Tell the model which column is 'output'
    #Also note columns that aren't purely numerical
    #Examples include ['nlp', 'date', 'categorical', 'ignore']
    "meta_data": {
      "avg_est_unit_cost_error": "output",
      "_id.funding_source": "categorical",
      "_id.department_name": "categorical",
      "_id.replacement_body_style": "categorical",
      "_id.replacement_make": "categorical",
      "_id.replacement_model": "categorical",
      "_id.procurement_plan": "categorical"
  }
}

trained_model = ai.run_experiment(experiment_design)
```

- __run_experiment(experiment_design):__ 

    - This function executes an experiment on selected model. Update experiment_design with parameters that fit your project.
    - The data parameter should be same as the refined training data. The model parameter must be a model subclass. 
    - The labels parameter indicates the column of the data dataframe to be predicted. 
    - For the prediction model, the meta-data must describe the column to be predicted and the types for non-numeric columns.


__Further Information on Model__


Machine learning model provides the intelligent behavior that you will publish as a microservice. The code in this section provides you with options for the model. You must select a model capable of using df to learn the behavior specified in the design section of the datastory. Run this function by defining each model type, then choose the model most appropriate for your datastory. Each model adheres to the specifications of a model. This allows any of the models to run according to the standard model lifecycle defined in run_experiment.

- __Prediction:__ This section defines a new type of model by creating a subclass of model. The prediction model learns to predict a particular outcome. It automatically optimizes parameters, selects features, selects an algorithm, and scores the results.

- __Regressor model:__ The regressor model makes a numeric prediction. Use this model when the design specification of the datastory requires the AI microservice to give a numerical outut prediction.

- __Classification model:__ The classification model makes a classification prediction. Use this model when the design specification of the datastory requires the AI microservice to give a categorical (text-based) outut prediction.

