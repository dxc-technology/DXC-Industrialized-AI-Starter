from dxc import ai
import pandas as pd
import pytest

@pytest.fixture
def df():
  url = "https://data.cincinnati-oh.gov/resource/ucjy-ykv4.json"
  df = ai.read_data_frame_from_remote_json(url)
  return df

def test_json_data_type(df):
  assert type(df) == type(pd.DataFrame())


@pytest.fixture
def df2():
  url = "https://raw.githubusercontent.com/npulagam/DataSets/main/Wine%20recipes%20data.json"
  df2 = ai.read_data_frame_from_remote_json(url)
  return df2

def test_json_data_type2(df2):
  assert type(df2) == type(pd.DataFrame())

def test_shape(df2):
  assert df2.shape == (39774, 67)


@pytest.fixture
def df3():
  url = 'https://raw.githubusercontent.com/dxc-technology/DXC-Industrialized-AI-Starter/master/dxc/ai/datasets/data/iris.csv'
  df3 = ai.read_data_frame_from_remote_csv(url)
  return df3

def test_columns(df3):
  cols = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
  assert list(df3.columns) == cols

def test_data_type_sepal_length(df3):
  assert df3['sepal length'].dtype == 'float64'

def test_data_type_sepal_width(df3):
  assert df3['sepal width'].dtype == 'float64'

def test_data_type_petal_length(df3):
  assert df3['petal length'].dtype == 'float64'

def test_data_type_petal_width(df3):
  assert df3['petal width'].dtype == 'float64'

def test_data_type_class(df3):
  assert df3['class'].dtype == 'O'

def test_shape(df3):
  assert df3.shape == (150, 5)
