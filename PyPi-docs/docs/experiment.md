# Run AI Experiments
---
An experiment trains and tests a machine-learning model. The code in this section runs a model through a complete lifecycle and saves the final model to the local drive. Run the code that defines a machine-learning model and its lifecycle. Design an experiment and execute it. Most of the work of choosing features and specific model parameters will be done automatically. The code will also automatically score each option and return the options with the best predictive performance.

Below is a example for run_experiment() function.
```python
experiment_design = {
    #model options include ['tpot_regression()', 'tpot_classification()', 'timeseries']
    "model": ai.tpot_regression(),
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

trained_model = ai.run_experiment(experiment_design, verbose = False, max_time_mins = 5, max_eval_time_mins = 0.04, config_dict = None, warm_start = False, export_pipeline = True, scoring = None)
```

- __ai.run_experiment(experiment_design):__

    - This function executes an experiment on selected model. Update experiment_design with parameters that fit your project.
    - The data parameter should be same as the refined training data. The model parameter must be a model subclass.
    - The labels parameter indicates the column of the data dataframe to be predicted.
    - For the prediction model, the meta-data must describe the column to be predicted and the types for non-numeric columns.


__Further Information on Model__


Machine learning model provides the intelligent behavior that you will publish as a microservice. The code in this section provides you with options for the model. You must select a model capable of using df to learn the behavior specified in the design section of the datastory. Run this function by defining each model type, then choose the model most appropriate for your data story. Each model adheres to the specifications of a model. This allows any of the models to run according to the standard model lifecycle defined in run_experiment.

## TPOT Classification/Regression:
Machine learning is  typically a very time-consuming and knowledge-intensive part of a data science problem. Auto-ml is not designed to replace the data scientist, but rather free her to work on more important aspects of the complete problem, such as acquiring data and interpreting the model results.[TPOT](https://epistasislab.github.io/tpot) is a Python library developed for automatic machine learning feature preprocessing, model selection, and hyperparameter tuning. AI Starter has integrated TPOT as one of its Auto Ml libraries.

Please refer the below parameter description for best utilization of Tpot classification and regression methods with AI Starter.<br>

**<code>verbose: True/False </code>** True - Prints more information and provide a progress bar; False - Prints nothing. <br>

**<code>max_time_mins:</code>** How many minutes the pipeline has to be optimized. The default value is 5 minutes. The maximum time better the results.<br>

**<code>max_eval_time_mins:</code>**How many minutes a single pipeline has to be evaluated. Setting this parameter to higher values will allow Auto_ml to evaluate more complex pipelines, but will also allow Auto_ml to run longer. Use this parameter to help prevent Auto_ml from wasting time on evaluating time-consuming pipelines.<br>

**<code>config_dict:</code>** Beyond the default configurations that come with Auto_ml, in some cases, it is useful to limit the algorithms and parameters that Auto_ml considers. For that reason, we allow users to provide Auto_ml with a custom configuration for its operators and parameters.<br>

 For example: config_dict = {'sklearn.ensemble.GradientBoostingRegressor':{}} <br> For more detailed examples and different configurations check [here](https://epistasislab.github.io/tpot/using/#customizing-tpots-operators-and-parameters). <br>

**<code>warm_start: True/False</code>** This parameter lets you restart and continue to evaluate pipelines from where it left off in previous execution. <br>

**<code>export_pipeline: True/False</code>** This parameter automatically exports the corresponding Python code for the optimized pipeline to a python file and saves the python file and encoded data_file in your current directory. <code>best_pipeline.py</code> will contain the Python code for the optimized pipeline. The default value for this parameter is 'True'. We suggest not changing the value as the optimized pipeline code will help to evaluate your model using model explainability which will be one of the tasks to achieve the AI Forensics badge.

**<code>scoring:</code>** This parameter is used to evaluate the quality of a given pipeline for the problem. By default, 'accuracy' is used for classification, and 'mean squared error' (MSE) is used for regression.

The following built-in scoring functions can be used for **Classification** Problem:

- accuracy, adjusted_rand_score, average_precision, balanced_accuracy,
- f1, f1_macro, f1_micro, f1_samples, f1_weighted
- neg_log_loss, precision etc. (suffixes apply as with ‘f1’)
- recall etc. (suffixes apply as with ‘f1’), ‘jaccard’ etc. (suffixes apply as with ‘f1’)
- roc_auc, roc_auc_ovr, roc_auc_ovo, roc_auc_ovr_weighted, roc_auc_ovo_weighted

The following built-in scoring functions can be used for **Regression** Problem:

- neg_median_absolute_error, neg_mean_absolute_error, neg_mean_squared_error, r2

If you need more knowledge on how to create custom scores please check [here](https://epistasislab.github.io/tpot/using/#scoring-functions)

__Timeseries model:__ The timeseries model automated the process for predicting future values of a signal using a machine learning approach. It allows forecasting a time series (or a signal) for future values in a fully automated way. Use this model when design specification of the data story requires to predict future values based on the time. [Here](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/blob/master/Examples/Time_series_Model.ipynb) is an example notebook for timeseries model.

## Deep Learning Model

DXC Industrialized AI starter has Deep Learning model for image classification.

Image classification is a supervised learning problem. A set of target classes are defined, and a model is trained with labeled images (train set). This trained model will identify and classifies new input into one of the target class.

This model can be used through three functions mentioned below:

1.	ai.create_training_data
2.	ai.split_normalize_data
3.	ai.image_classifier

__ai.create_training_data:__ This function reads each folder and each image from the path provided and will convert image to an array. It will also resize your image to the size provided, default size is 100. This function takes list of image categories, image folder directory/path and resize size. This function return features and labels.

__ai.split_normalize_data:__ This function split your training data into train and test based on the size of test provided. Default test size will be 0.20. Along with splitting the data to train and test, this function will also normalize the data.Th is function takes features, labels, test size (default 0.20), category count and image size (default 100).This function returns train and test sets.

__ai.image_classifier:__ This function compiles the model with the image size and number of categories provided. It adds the input, hidden and output layers and compiles the model. Here returned model is trained with train data sets and further used for prediction.

This [example notebook](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/blob/master/Examples/DL_Image_classifier.ipynb) helps you to understand how to use this model from AI starter library.

## Clustering Model

Clustering model is an unsupervised technique, which performs the clustering on the dataset depending on the attributes without knowing any information about the output. Our aim is to retrieve the hidden clusters from the data, our model performs the basic auto clustering based on the silhouette score. The Clustering models that are used in the library are:

- Affinity propagation
- K-Means
- DBSCAN

The best method out of this is being selected based on the scores and the trained model of the same is returned as the output. [Here](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/blob/master/Examples/Clustering_ipynb.ipynb) is the example notebook for clustering model.
