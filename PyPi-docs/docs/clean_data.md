#Clean  Raw Data
---

Below code snippet helps to clean raw data.
```python
	clean_data = ai.clean_dataframe(df)
```

- This method imputes missing data, cleans the column headings, removes empty rows and columns, anonymizes text, and casts fields to their proper data type. 
- Except for the data, every input field for the clean_dataframe is optional. By default, the method will not impute missing data. If instructed, the clean_dataframe will replace missing numeric fields with the mean value and replace missing categorical fields with the mode.



__ai.clean_dataframe(df, impute = False, text_fields = [], date_fields = [], numeric_fields = [], categorical_fields = []):__
	
	
The above function performs the following process:

- The column names are transformed to lower case and spaces are removed.
- If any of the rows or columns with total null values are removed completely.
- For text fields, the cleaner removes harmful characters, removes personal identifiers, converts to lowercase
- For object field types(categorical field), the KNN model is implemented with a default value of K as 2 to fill the missing values. KNN model imputes the missing values with the prediction based on all the other attributes. This makes data more reliable and meaningful as all the values are implemented using a prediction model against all the attributes.
- For the KNN model to run, the object datatypes are encoded into numerical values, and predictions are calculated based on the encoded values and after the predictions are made, values are decoded and converted back to original values for user convenience.
- For Numerical field types, the skewness of the column is calculated. If the skewness is within the range of -1 to 1, the mean of the column is used to impute the missing values otherwise median is used to impute the missing values.
