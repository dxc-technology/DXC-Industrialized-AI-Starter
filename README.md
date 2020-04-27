![DXC](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/blob/master/dxc%20image.png)

# DXC Industrialized AI Starter

DXC Indusrialized AI Starter makes it easier to build and deploy Indusrialized AI. This Library does the following:

- Access, clean, and explore raw data
- Build data pipelines
- Run AI experiments
- Publish microservices

## Installation

In order to install and use above library please use the below code snippet:
```
1. pip install DXC-Industrialized-AI-Starter
2. from dxc import ai
```

## Getting Started

### Access, Clean, and Explore Raw Data

Here's a quick example of using the library to access, clean, and explore raw data.

```
#Access raw data
df = ai.read_data_frame_from_remote_json(json_url)
df = ai.read_data_frame_from_remote_csv(csv_url)
df = ai.read_data_frame_from_local_json()
df = ai.read_data_frame_from_local_csv()
df = ai.read_data_frame_from_local_excel_file()

#Clean data
raw_data = ai.clean_dataframe(df)

#Explore raw data
ai.visualize_missing_data(raw_data)
ai.explore_features(raw_data)
ai.plot_distributions(raw_data)
```

### Build Data Pipelines

Below example showcases how to build a data pipeline. In order to get started,you need to first have an  <a href= "https://account.mongodb.com/account/register" target="_blank">MongoDB</a> account which you can signup for free and create a database "connection_string" and specify those details in the data_layer below.


```
#Insert data into MongoDB:
data_layer = {
    "connection_string": "<your connection_string>",
    "collection_name": "<your collection_name>",
    "database_name": "<your database_name>"
}
wrt_raw_data = ai.write_raw_data(data_layer, raw_data, date_fields = [])
```
This code instructs the data store on how to refine the output of raw_data into something that can be used to train a machine-learning model. Update data_pipeline() with code with an aggregation pipeline that fits your project. The refined data will be stored in the  Pandas dataframe. Make sure the output is what you want before continuing. Below is the example for creating pipeline:
```
pipeline = [
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

df = ai.access_data_from_pipeline(wrt_raw_data, pipeline)
```
For more detailed explaination <a href= "https://dxc-technology.github.io/DXC-Industrialized-AI-Starter/data_pipeline/" target="_blank">click here</a>

### Run AI Experiments

Sample code snippet to run an AI Experiment

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

### Publish Microservice

Below is the example for publishing a Microservice. In order to  design the microservice, you must [create an Algorithmia account](https://algorithmia.com/signup). This code defines the parameters needed to build and delpoy a microservice based on the trained model. Update microservice_design with parameters appropriate for your project.
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

# publish the micro service and display the url of the api
api_url = ai.publish_microservice(microservice_design, trained_model)
print("api url: " + api_url)
```

## Docs

For detailed and complete documentation, please <a href="https://dxc-technology.github.io/DXC-Industrialized-AI-Starter/access_clean_explore/" target="_blank">click here</a>


### Example of colab notebook


<a href="https://colab.research.google.com/drive/1EV_Q09B-bppGbEehBgCvsv_JIM87T_n1" target="_blank">Here</a> is an  detailed and in-depth example of the google colab notebook 

### Contributing Guide

To know more about the contribution and guidelines please <a href="https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/blob/master/CONTRIBUTING.md" target="_blank">click here</a>


### Reporting Issues
If you find any issues, feel free to report them <a href="https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/issues" target="_blank">here</a> with clear description of your issue.
