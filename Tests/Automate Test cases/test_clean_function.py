from dxc import ai
import pandas as pd
import pytest

# read and clean the data
@pytest.fixture
def clean_df():
  url = 'https://raw.githubusercontent.com/npulagam/DataSets/main/healthcare-dataset-stroke-data.csv'
  df = ai.read_data_frame_from_remote_csv(url)
  text_fields = ['Name']
  categorical_fields = ['gender', 'EverMarried', 'Work Type', 'Residence_type', 'smoking status', 'Hypertension', 'heart_disease', 'stroke']
  numeric_fields = ['id', 'AGE', 'avg_glucose_level', 'BMI']
  #date_fields = ['report_date']
  date_fields = []
  impute = True
  clean_df = ai.clean_dataframe(df, impute, text_fields, date_fields, numeric_fields, categorical_fields)
  return clean_df

# Testing for Null values in the clean dataframe 
def test_null_values(clean_df): 
  assert clean_df.isnull().values.any() == False
  assert clean_df.isnull().sum().sum() == 0

# Testing for NaN values in the clean dataframe 
def test_nan_values(clean_df):
  assert clean_df.isna().values.any() == False
  assert clean_df.isna().sum().sum() == 0

# Test for column names with camelcase
def test_camelcase_col(clean_df):
  cols = clean_df.columns
  assert ('EverMarried' not in cols) and ('evermarried' in cols) == True

# Test for column names with upper case
def test_uppercase_col(clean_df):
  cols = clean_df.columns
  assert ('AGE' not in cols) and ('age' in cols) == True
  assert ('BMI' not in cols) and ('bmi' in cols) == True
  assert ('Name' not in cols) and ('name' in cols) == True

# Test for column names containing spaces
def test_spaces_col(clean_df):
  cols = clean_df.columns
  assert ('smoking status' not in cols) and ('smoking_status' in cols) == True

# Test for column names containing Titlecase
def test_titlecase_col(clean_df):
  cols = clean_df.columns
  assert ('Work Type' not in cols) and ('work_type' in cols) == True
  assert ('Report Date' not in cols) and ('report_date' in cols) == True

# Test for column names containing underscore character
def test_underscore_col(clean_df):
  cols = clean_df.columns
  assert ('Residence_type' not in cols) and ('residence_type' in cols) == True

# Test for column names containing hyphen character
def test_hyphen_col(clean_df):
  cols = clean_df.columns
  assert ('Avg-glucose-level' not in cols) and ('avg_glucose_level' in cols) == True

# Test for column names containing slash character
def test_slash_col(clean_df):
  cols = clean_df.columns
  assert ('heart/disease' not in cols) and ('heart_disease' in cols) == True
  
# Testcases for data type of the column 
def test_gender_col_dtype(clean_df):
  assert clean_df['gender'].dtype == 'category'

def test_evermarried_col_dtype(clean_df):
  assert clean_df['evermarried'].dtype == 'category'

def test_work_type_col_dtype(clean_df):
  assert clean_df['work_type'].dtype == 'category'

def test_residence_type_col_dtype(clean_df):
  assert clean_df['residence_type'].dtype == 'category'
  
def test_smoking_status_col_dtype(clean_df):
  assert clean_df['smoking_status'].dtype == 'category'

def test_hypertension_col_dtype(clean_df):
  assert clean_df['hypertension'].dtype == 'category'

def test_heart_disease_col_dtype(clean_df):
  assert clean_df['heart_disease'].dtype == 'category'

def test_stroke_col_dtype(clean_df):
  assert clean_df['stroke'].dtype == 'category'  

def test_id_col_dtype(clean_df):
  assert clean_df['id'].dtype == 'float64'  

def test_bmi_col_dtype(clean_df):
  assert clean_df['bmi'].dtype == 'float64'  

def test_age_col_dtype(clean_df):
  assert clean_df['age'].dtype == 'float64'  

def test_avg_glucose_level_col_dtype(clean_df):
  assert clean_df['avg_glucose_level'].dtype == 'float64'   

def test_name_dtype(clean_df):
  assert clean_df['name'].dtype == 'O'

def test_report_date_dtype(clean_df):
  assert clean_df['report_date'].dtype == 'O'

# Validating the data form clean function for text column 
def test_cleaned_text_data(clean_df):
  assert clean_df['name'][1] == '{{name-1}}'
