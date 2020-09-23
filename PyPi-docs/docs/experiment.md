# Run AI Experiments
---
An experiment trains and tests a machine-learning model. The code in this section runs a model through a complete lifecycle and saves the final model to the local drive. Run the code that defines a machine-learning model and its lifecycle. Design an experiment and execute it. Most of the work of choosing features and specific model parameters will be done automatically. The code will also automatically score each option and return the options with the best predictive performance.

Below is a example for run_experiment() function.
```python
experiment_design = {
    #model options include ['regression()', 'classification()', 'timeseries']
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

- __ai.run_experiment(experiment_design):__

    - This function executes an experiment on selected model. Update experiment_design with parameters that fit your project.
    - The data parameter should be same as the refined training data. The model parameter must be a model subclass.
    - The labels parameter indicates the column of the data dataframe to be predicted.
    - For the prediction model, the meta-data must describe the column to be predicted and the types for non-numeric columns.


__Further Information on Model__


Machine learning model provides the intelligent behavior that you will publish as a microservice. The code in this section provides you with options for the model. You must select a model capable of using df to learn the behavior specified in the design section of the datastory. Run this function by defining each model type, then choose the model most appropriate for your data story. Each model adheres to the specifications of a model. This allows any of the models to run according to the standard model lifecycle defined in run_experiment.

- __Regressor model:__ The regressor model makes a numeric prediction. Use this model when the design specification of the data story requires the AI microservice to give a numerical output prediction.

- __Classification model:__ The classification model makes a classification prediction. Use this model when the design specification of the data story requires the AI microservice to give a categorical (text-based) output prediction.

- __Timeseries model:__ The timeseries model automated the process for predicting future values of a signal using a machine learning approach. It allows forecasting a time series (or a signal) for future values in a fully automated way. Use this model when design specification of the data story requires to predict future values based on the time. [Here](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/blob/master/Examples/Time_series_Model.ipynb) is an example notebook for timeseries model.

- __Prediction:__ This section defines a new type of model by creating a subclass of model. The prediction model learns to predict a particular outcome. It automatically optimizes parameters, selects features, selects an algorithm, and scores the results.

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
