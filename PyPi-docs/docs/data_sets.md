# Load Data

Finding the right or sample dataset is one of the important tasks for those who are starting to work on Machine learning and AI. Though we have many datasets readily available finding the right dataset, loading, and using it can always be challenging especially for beginners. DXC Industrialized AI Starter makes this easy by providing a few data sets and functions to load them easily without any difficulties.

Below code, snippet helps you to load and view the datasets from this library.

```python
# To know more details about the dataset
print(ai.load_data_details('bike_sharing_data'))

# To load the data sets into pandas dataframe
df = ai.load_data('bike_sharing_data')
df.head()
```

For loading the datasets from this library we use below two functions.

1. __ai.load_data(filename):__ It takes a filename as input and loads that particular dataset into your notebook and return a pandas data frame.
2. __ai.load_data_details(filename):__ This function loads the dataset details and print  information. This function takes a filename as input. The information retrieved helps the user to understand the dataset and the significance of those columns in the dataset.

A list of datasets available in AI Starter is provided below.

An example note on how to use these functions is placed under the “Examples” folder in the git repository.

#### Available Datasets

Below datasets are available in the DXC Industrialized AI Starter library.

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