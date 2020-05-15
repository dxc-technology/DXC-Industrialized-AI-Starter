# Access, Clean and Explore
---
## Access raw data

Below code snippets help to bring in raw data from either a remote source or from your local machine into a dataframe.

```
	df = ai.read_data_frame_from_remote_json(json_url)
	df = ai.read_data_frame_from_remote_csv(csv_url)
```

Get raw data from your __local machine__ by opening up a file system browser, identifying a file, and importing the selected file.
```
	df = ai.read_data_frame_from_local_csv()
	df = ai.read_data_frame_from_local_excel_file()
```	
- __read_data_frame_from_remote_json(json_url):__ It reads JSON files from a URL and also flattened (in the case of nested data) the json data and cast into a pandas data frame.

- __read_data_frame_from_remote_csv(csv_url, col_names = [], delim_whitespace=False, header = 'infer'):__ It allows you to read character-delimited (commas, tabs, spaces) data from a URL. Expect csv_url parameter remaining all are optional.

- __read_data_frame_from_local_csv(col_names = [], delim_whitespace=False, header = 'infer'):__ This method allows you to import local character-delimited (commas, tabs, spaces) files. All parameters are optional. By default, the function will infer the header from the data, but an explicit header can be specified.

- __read_data_frame_from_local_excel_file():__ This function allows you to import XLSX files. When the file explorer is launched, you must select an XLSX file or the function will result in an error.

## Clean raw data
---

Below code snippet helps to clean raw data.
```
	raw_data = ai.clean_dataframe(df)
```
- __clean_dataframe(df, impute = False, text_fields = [], date_fields = [], numeric_fields = [], categorical_fields = []):__
	- This method imputes missing data, cleans the column headings, removes empty rows and columns, anonymizes text, and casts fields to their proper data type. 
	- Except for the data, every input field for clean_dataframe is optional. By default the method will not impute missing data. If instructed, clean_dataframe will replace missing numeric fields with the mean value and replace missing categorical fields with the mode.

## Explore raw data
---
Below code snippet helps to explore and visualize raw data.
```
	ai.visualize_missing_data(raw_data)
	ai.explore_features(raw_data)
	ai.plot_distributions(raw_data)
```
- __explore_features(df):__ 
	- It visualizes the relationships between all features in a given data frame. Areas of heat show closely-related features.
	- This visualization is useful when trying to determine which features can be predicted and which features are needed to make the prediction.
	- It is useful to explore the correlations between features in the raw data. Use this visualization to form a hypothesis about how the raw data can be used. It may be necessary to enrich raw data with other features to increase the number and strength of correlations.

- __visualize_missing_data(df):__ 

	- It creates a visual display of missing data in a data frame. Each column of the data frame is shown as a column in the graph. Missing data is represented as horizontal lines in each column.
	- This visualization is useful when determining whether or not to impute missing values or for determining whether or not the data is complete enough for analysis. 
	- It is useful to visualize missing fields in your raw data. Determine if imputing is necessary.

- __plot_distributions(df):__ 
	- It creates a distribution graph for each column in a given data frame. 
	- Graphs for data types that cannot be plotted on a distribution graph without refinement (types like dates), will show as blank in the output. 
	- This visualization is useful for determining skew or bias in the source data. Use plot_distributions to show the distributions for each feature in raw_data. 
	- Depending on raw data, this visualization may take several minutes to complete. Use the visualization to determine if there is a data skew that may prevent proper analysis or useful insight.
