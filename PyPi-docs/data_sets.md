# Load Data

Finding right or sample data set is one of the important tasks for those who are starting to work on Machine learning and AI. Though we have many datesets readily available finding right dataset, loading and using it can always be challangeing specically for beginners. DXC Industrialized AI Starter make this easy by providing few data sets and functions to load them easily without any difficulties.

Below code sinpet helps you to load and view the datsets from this library.

```python
# To know more details about the dataset
print(ai.load_data_details('bike_sharing_data'))

# To load the data sets into pandas dataframe
df = ai.load_data('bike_sharing_data')
df.head()
```

For loading the datasets from this library we use below two functions.

1. __ai.load_data(filename):__ It takes filename as input and loads that particular datset into your notebook and return a pandas dataframe.
2. __ai.load_data_details(filename):__ This function loads the dataset details and print  information. This function takes filename as input. The information retrieved helps user to understand the dataset and significance of those columns in dataset.

List of datasets available in AI Starter are provided below.

Example note on how to use this functions is placed under “Examples” folder in git repository.

#### Available Datasets

Below datasets are availabe in DXC Industrialized AI Starter library.

|Dataset Name | Filename to load|
|------------- |----------------|
|New York city Airbnb data for the year 2019 |ab_nyc_2019|
|Abalone data | abalone|
|Auto mobiles Imports data| auto_imports|
|Bike sharing Dataset | bike_sharing |
|Breast cancer data | breast_cancer|
|German credit data | german |
|Boston Housing dataset| housing |
|Optical recognition of handwritten digits | hand_written_digits |
|Breast cancer dataset obtained from the University of Wisconsin| breast_cancer_wisconsin |
|Horse colic data | horse_colic|
| Wine quality white | winequality_white |
|Boston Housing dataset with 163 attributes| house_prices |
|IBM employee attrition data | hr_employee_attrition |
|Johns Hopkins University Ionosphere data | ionosphere|
|Iris plants data | iris |
|Pima Indians diabetes data | pima_indians_diabetes |
| Sonar signals data | sonar |
| Wheat seeds data | wheat_seeds |
| Wine quality red | winequality_red |
| MNIST data | mnist |


 
