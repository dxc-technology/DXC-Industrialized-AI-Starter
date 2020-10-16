# Publish Microservice 
---
The DXC AI Starter library makes it easy to publish your models as working microservices. By default, the DXC AI Starter library uses free tier of [Algorithmia](https://algorithmia.com/signup) to publish models as microservices. To provide the information required to design the microservice, you must:

- create an <a href = "https://algorithmia.com/signin#credentials" target="_blank"> Algorithmia</a> account 
- create an API key with BOTH "Read & Write Data" and "Manage Algorithms" permissions enabled
- create an algorithm user name

```python
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

- __publish_microservice(microservice_design, trained_model):__
	
	- The code in this section prepares an execution environment for the microservice, builds a microservice using the machine-learning model, deploys the microservice into the execution environment, and publishes an API endpoint for the microservice.

	- The work of creating the microservice and deploying it will be done automatically. The code will also automatically handle the source code repository management.

	- This code defines the parameters needed to build and deploy a microservice-based on the trained model.
	- Update microservice_design with parameters appropriate for your project. The parameters must contain valid keys, namespaces, and model paths from Algorithmia.
 