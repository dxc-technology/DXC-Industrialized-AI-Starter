# Explore Data
---

## Explore raw data

Below code, snippet helps to explore and visualize raw data.
```
	ai.visualize_missing_data(raw_data)
	ai.explore_features(raw_data)
	ai.plot_distributions(raw_data)
```
- __ai.explore_features(df):__
	- It visualizes the relationships between all features in a given data frame. Areas of heat show closely-related features.
	- This visualization is useful when trying to determine which features can be predicted and which features are needed to make the prediction.
	- It is useful to explore the correlations between features in the raw data. Use this visualization to form a hypothesis about how raw data can be used. It may be necessary to enrich raw data with other features to increase the number and strength of correlations.

- __ai.visualize_missing_data(df):__

	- It creates a visual display of missing data in a data frame. Each column of the data frame is shown as a column in the graph. Missing data is represented as horizontal lines in each column.
	- This visualization is useful when determining whether or not to impute missing values or for determining whether or not the data is complete enough for analysis.
	- It is useful to visualize missing fields in your raw data. Determine if imputing is necessary.

- __ai.plot_distributions(df):__
	- It creates a distribution graph for each column in a given data frame.
	- Graphs for data types that cannot be plotted on a distribution graph without refinement (types like dates), will show as blank in the output.
	- This visualization is useful for determining skew or bias in the source data. Use plot_distributions to show the distributions for each feature in raw_data.
	- Depending on raw data, this visualization may take several minutes to complete. Use the visualization to determine if there is a data skew that may prevent proper analysis or useful insight.

## Visualize complete data

```python
report = ai.explore_complete_data(df)
report.to_notebook_iframe()
```

__ai.explore_complete_data(df):__ This function generates profile reports from a pandas DataFrame for exploratory data analysis. For each column, the following statistics are presented in an interactive HTML report. You can download that as an HTML report and share it with others easily. [Here](https://nbviewer.jupyter.org/github/dxc-technology/DXC-Industrialized-AI-Starter/blob/c58754247060262ac0949396e48f71861cb79d4e/Examples/Complete_Data_Visualization.ipynb) is the example notebook to know the usage of this function. 

- __Type inference:__ detect the types of columns in a DataFrame.
- __Essentials:__ type, unique values, missing values
- Quantile statistics like minimum value, Q1, median, Q3, maximum, range, interquartile range
- Descriptive statistics like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
- Most frequent values
- Histogram
- Correlations highlighting of highly correlated variables, Spearman, Pearson, and Kendall matrices
- Missing values matrix, count, heatmap, and dendrogram of missing values
- Text analysis learn about categories (Uppercase, Space), scripts (Latin, Cyrillic), and blocks (ASCII) of text data.
- File and Image analysis extract file sizes, creation dates, and dimensions and scan for truncated images or those containing EXIF information.
