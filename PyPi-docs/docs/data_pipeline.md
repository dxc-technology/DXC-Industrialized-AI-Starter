# Build Data Pipelines
---
## Insert data into MongoDB

Pipelines are a standard way to process your data towards modeling and interpreting. By default, the DXC AI Starter library uses the free tier of [MongoDB Atlas](https://account.mongodb.com/account/register) to store raw data and execute pipelines. This code defines the meta-data needed to connect to Mongo DB Atlas and create a new datastore cluster. This is where you define basic information about the location of the cluster and the collection and database to use. Update this code with information appropriate to your project. To provide the information required in data_layer, you must:

- Create a <a href="https://account.mongodb.com/account/login" target="_blank"> MongoDb </a> Atlas account
- Create a cluster
- Create a user
- Generate a connection string

__Note:__ When you configure the IP whitelist for your cluster, choose to allow a connection from anywhere. When creating the database connection string, choose the Python driver version 3.4 or later.

Example:
```python
data_layer = {
    "connection_string": "<your connection_string>",
    "collection_name": "<your collection_name>",
    "database_name": "<your database_name>",
    "data_source":"<Source of your datset>",
    "cleaner":"<whether applied cleaner yes/no >"
}

wrt_raw_data = ai.write_raw_data(data_layer, raw_data, date_fields = [])
```


__ai.write_raw_data(data_layer, raw_data, date_fields = [ ]):__ 

- This function handles Mongo DB Atlas automatically.
- Use write_raw_data function from ai library to convert Arrow dates to Strings data types
- It also transfers the raw data into the database and collection.
- It also stores metadata details, which is created as a separate collection, and it stores the information about each version along with their time of insertion.

__Version control in Mongo DB:__

DXC AI Starter is being equipped with the version control functionality, wherein the documents(data frames) inserted into the mongo are saved automatically as versions. The latest version is always in sync with the retrieved document. The versions are made with an underscore(_) and a number that is directly proportional to the number of times the document is changed. This helps in retrieving back the previous versions of the data.




## Build Pipeline
---

Once raw data is stored, you can run pipelines to transform the data. Please refer to the syntax of [MongDB pipelines](https://docs.mongodb.com/manual/core/aggregation-pipeline/) for the details of how to write a pipeline. Below is an example of creating and executing a pipeline.

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

- __ai.access_data_from_pipeline(write_raw_data, pipeline):__ This function instructs the datastore on how to refine the output of raw data into something that can be used to train a machine-learning model. The refined data will be stored in the df Pandas data frame. Make sure the output is what you want before continuing.