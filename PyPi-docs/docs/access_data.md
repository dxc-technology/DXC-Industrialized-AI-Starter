# Access raw data
---
Below code snippets help to bring in raw data from either a remote source or from your local machine into a data frame.

```python
	df = ai.read_data_frame_from_remote_json(json_url)
	df = ai.read_data_frame_from_remote_csv(csv_url)
```

Get raw data from your __local machine__ by opening up a file system browser, identifying a file, and importing the selected file.
```python
	df = ai.read_data_frame_from_local_csv()
	df = ai.read_data_frame_from_local_excel_file()
```	

## Access CSV data

__ai.read_data_frame_from_remote_csv__(csv_url, col_names = [], names=None, sep=',',  delim_whitespace=False, header = 'infer', skiprows=None, error_bad_lines=True, encoding=None)__

- It allows you to read character-delimited (commas, tabs, spaces) data from a URL. Expect csv_url parameter remaining all are optional.
- col_names: array-like, optional
- sep: str, default ‘,’
- names: array-like, optional
- header: int, list of int, default ‘infer’
- delim_whitespace: True or False
- skiprows: list-like, int or callable, optional
- error_bad_linesbool, default None
- encoding: str, optional - Encoding to use for UTF when reading/writing (ex. ‘utf-8’)

__ai.read_data_frame_from_local_csv(col_names = [], sep=',', delim_whitespace=False, header = 'infer', names = None, skiprows=None, error_bad_lines=True, encoding=None):__ 

- This method allows you to import local character-delimited (commas, tabs, spaces) files. All parameters are optional. By default, the function will infer the header from the data, but an explicit header can be specified.

## Access JSON data

__ai.read_data_frame_from_remote_json(json_url)__
 
 - It reads JSON files from a URL and also flattened (in the case of nested data) the json data and cast into a pandas data frame.

## Access Excel data

__ai.read_data_frame_from_local_excel_file()__ 

- This function allows you to import XLSX files. When the file explorer is launched, you must select an XLSX file or the function will result in an error.


