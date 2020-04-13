# DXC Industrialized AI Starter 1.0 documentation
## Read data

The functions are designed to bring in data from either a remote source or from your local machine. Data from remote sources are accessed through URLs. Data from your local machine is read by opening up a file system browser, identifying a file, and importing the selected file. Each method returns  Pandas data frame.

### read_data_from_remote_json(URL):

The read_data_frame_from_remote_json function reads JSON files from a URL. JSON data is flattened (in the case of nested data) and cast into Pandas data frame.

### read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):

This function allows you to import local character-delimited (commas, tabs, spaces) files. All parameters are optional. By default, the function will infer the header from the data, but an explicit header can be specified.

### read_data_frame_from_remote_csv(csv_url, col_names = [], delim_whitespace=False, header = 'infer'):

This function works the same way as read_data_frame_from_local_csv function except that it reads the file from a URL instead of from your local machine. The URL is required.

### read_data_frame_from_local_excel_file():

This function allows you to import XLSX files. When the file explorer is launched, you must select an XLSX file or the function will result in an error.

## Clean data

### clean_dataframe(df, impute = False, text_fields = [], date_fields = [], numeric_fields = [], categorical_fields = []):

The clean_dataframe method imputes missing data, cleans the column headings, removes empty rows and columns, anonymizes text, and casts fields to their proper data type. Except for the data, every input field for clean_dataframe is optional. By default the method will not impute missing data. If instructed, clean_dataframe will replace missing numeric fields with the mean value and replace missing categorical fields with the mode.

## Explore the raw data

you can explore the data to determine how it can be used. This below functions provides methods for visualizing the data in useful ways

### explore_features(df):

It visualizes the relationships between all features in a given data frame. Areas of heat show closely-related features. This visualization is useful when trying to determine which features can be predicted and which features are needed to make the prediction.

Use explore_features to explore the correlations between features in the raw data. Use the visualization to form a hypothesis about how the raw data can be used. It may be necessary to enrich raw data with other features to increase the number and strength of correlations. If necessary, refine raw data and repeat this analysis.

### visualize_missing_data(df):

It creates a visual display of missing data in a data frame. Each column of the data frame is shown as a column in the graph. Missing data is represented as horizontal lines in each column. This visualization is useful when determining whether or not to impute missing values or for determining whether or not the data is complete enough for analysis.

Use visualize_missing_data to visualize missing fields in your raw data. Determine if imputing is necessary. Refine raw data, if necessary, and repeat this analysis.

### plot_distributions(df):

It creates a distribution graph for each column in a given data frame. Graphs for data types that cannot be plotted on a distribution graph without refinement (types like dates), will show as blank in the output. This visualization is useful for determining skew or bias in the source data.

Use plot_distributions to show the distributions for each feature in raw_data. Depending on raw data, this visualization may take several minutes to complete. Use the visualization to determine if there is a data skew that may prevent proper analysis or useful insight. If necessary, refine raw data and repeat this analysis.

## Build a data pipeline

A data pipeline takes raw data and turns it into refined data that can be used to train and score a machine-learning model. The code in this section takes the output of raw_data() and puts it into a data store. It instructs the data store to refine the raw data into training data. It extracts the training data for use in training a machine-learning model. Specifiy the details for how to connect to the data store. Run the code to connect to the data store. "Write code" that instructs the data store on how to refine the raw data. Run the code to extract the refined data. This code assumes that Mongo DB Atlas is the data store.

You will be using <a href="https://account.mongodb.com/account/login"> MongoDb </a> as your data store. This video provides a general overview of MongoDB. The document model of MongoDB breaks from the traditional relational model of common relational databases. This video describes the basic idea behind the document model. It also describes MongoDb clusters and the methods used to scale. It introduces MongoDB Atlas, which you will be using in the remainder of this notebook.

[![Document model](https://img.youtube.com/vi/EE8ZTQxa0AM/0.jpg)](https://www.youtube.com/watch?v=EE8ZTQxa0AM)

This video provides an overview of <a href="https://account.mongodb.com/account/login">Mongo DB Atlas</a>. It provides an explanation of the software. It walks you through the basic tasks of setting up an account and generating the proper connection credentials. Watch this video if you are unfamiliar with Mongo DB Atlas. This video should be removed or replaced if the data is stored using something other than Mongo DB Atlas.

[![Overview of Mongo DB](https://img.youtube.com/vi/rPqRyYJmx2g/0.jpg)](https://www.youtube.com/watch?v=rPqRyYJmx2g)

### write_raw_data(data_layer, raw_data, date_fields):

This code defines the meta-data needed to connect to Mongo DB Atlas and create a new data store cluster. This is where you define basic information about the location of the cluster and the collection and database to use. Update this code with information appropriate to your project. This code assumes that the data store is Mongo DB Atlas. In order to provide the information required in data_layer, you must:

- Create a MongoDB Atlas account
- Create a cluster
- Create a user
- Generate a connection string
__Note:__ When you configure the IP whitelist for your cluster, choose to allow a connection from anywhere. When creating the database connection string, choose the Python driver version 3.4 or later.

specify the data layer in your function in below format.
```
data_layer = {
    "connection_string": "<your connection_string>",
    "collection_name": "<your collection_name>",
    "database_name": "<your database_name>"
}
```
## Ingest and clean data

This video provides an overview of how to create aggregation pipelines in Mongo DB Atlas. It describes the basic concepts and walks you through example pipelines. Watch this video if you are unfamiliar with Mongo DB Atlas aggregation pipelines.

[![creating aggregation pipelines in Mongo DB](https://img.youtube.com/vi/Kk6Er0c7srU/0.jpg)](https://www.youtube.com/watch?v=Kk6Er0c7srU)

### access_data_from_pipeline(write_raw_data, pipe):

This code instructs the data store on how to refine the output of raw data into something that can be used to train a machine-learning model.The refined data will be stored in the df Pandas dataframe. Make sure the output is what you want before continuing.

Below is a example for defining pipe(aggregation pipeline) in your function.
```
pipe = [
        {
            '$group':{
                '_id': {
                    "funding_source":"$funding_source",
                    "request_type":"$request_type",
                    "department_name":"$department_name",
                    "replacement_body_style":"$replacement_body_style",
                    "equipment_class":"$equipment_class",
                    "replacement_make":"$replacement_make",
                    "replacement_model":"$replacement_model",
                    "procurement_plan":"$procurement_plan"
                    },
                "avg_est_unit_cost":{"$avg":"$est_unit_cost"},
                "avg_est_unit_cost_error":{"$avg":{ "$subtract": [ "$est_unit_cost", "$actual_unit_cost" ] }}
            }
        }
]
  ```

## Run an experiment

An experiment trains and tests a machine-learning model. The code in this section runs a model through a complete lifecycle and saves the final model to the local drive. Run the code that defines a machine-learning model and its lifecycle. Design an experiment and execute it. Most of the work of choosing features and specific model parameters will be done automatically. The code will also automatically score each option and return the options with the best predictive performance.

### run_experiment(experiment_design):

Below is a example for experiment_design in run_experiment() function.
```
experiment_design = {
    #model options include ['regression()', 'classification()']
    "model": regression(),
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
```

__The ML model and lifecycle__
The code in this section defines what we mean by a machine-learning model and the lifecyle that all models will go through. The model class defines a basic machine-learning model. All machine learning models must be a subclass of model. The run_experiment function takes in subclasses of model and defines the lifecycle of a model.

__Select a model__
The model provides the intelligent behavior that you will publish as a microservice. The code in this section provides you with options for the model. Each code block defines a different type of model. You must select a model capable of using df to learn the behavior specified in the design section of the datastory. Run this function by defining each model type, then choose the model most appropriate for your datastory. Each model adheres to the specifications of a model. This allows any of the models to run according to the standard model lifecycle defined in run_experiment.

_Prediction model:_ This section defines a new type of model by creating a subclass of model. The prediction model learns to predict a particular outcome. It automatically optimizes parameters, selects features, selects an algorithm, and scores the results.

_Regressor model:_ The regressor model makes a numeric prediction. Use this model when the design specification of the datastory requires the AI microservice to give a numerical outut prediction.

_Classification model:_ The classification model makes a classification prediction. Use this model when the design specification of the datastory requires the AI microservice to give a categorical (text-based) outut prediction.

__Execute the experiment__
This code executes an experiment by running run_experiment() on a model. Update experiment_design with parameters that fit your project. The data parameter should remain df-- the refined training data. The model parameter must be a model subclass. The labels parameter indicates the column of the data dataframe to be predicted. For the prediction model, the meta-data must describe the column to be predicted and the types for non-numeric columns.

## Publish a Microservice 

Insights are delivered through microservices with published APIs. The code in this section prepares an execution environment for the microservice, builds a microservice using the machine-learning model, deploys the microservice into the execution environment, and publishes an API enpoint for the microservice. Design the microservice and deploy it. The work of creating the microservice and deploying it will be done automatically. The code will also automatically handle the source code reposity management.

This video provides an overview of the algorithm execution environment provided by Algorithmia. It describes the basic concept of the Algorithmia AI Layer and walks you through publishing a microservice. Watch this video if you are unfamiliar with publishing microservices using Algorithmia. This video should be removed or replaced if the microservices are run using something other than Algorithmia.

[![overview of algorithm](https://img.youtube.com/vi/56yt2Bouq0o/0.jpg)](https://www.youtube.com/watch?v=56yt2Bouq0o)

### publish_microservice(microservice_design, trained_model):

__Configure the microservice execution environment__

The execution environment is where the micorservice runs. This code assumes that the microservice execution environment is Algorithmia.  In order to provide the information required to design the microservice, you must:
- create an Algorithmia account
- create an <a href = "https://algorithmia.com/signin#credentials"> API key</a> with BOTH "Read & Write Data" and "Manage Algorithms" permissions enabled
- create an algorithm user name

__Design the microservice__
This code defines the parameters needed to build and delpoy a microservice based on the trained model. Update microservice_design with parameters appropriate for your project. The parameters must contain valid keys, namespaces, and model paths from Algorithmia.

```
trained_model is the output of run_experiment() function
microservice_design = {
    "microservice_name": "<Name of your microservice>",
    "microservice_description": "<Brief description about your microservice>",
    "execution_environment_username": "<Algorithmia username>",
    "api_key": "<your api_key>",
    "api_namespace": "<your api namespace>",   
    "model_path":"<your model_path>"
}

```
