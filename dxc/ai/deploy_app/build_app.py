from dxc.ai.global_variables import globals_file
import pickle
import pandas as pd

def generate_req_files():
    tpot_data = pd.read_csv('/content\data_file.csv')

    # Save encoder
    if globals_file.run_experiment_encoder_used:
        pickle.dump(globals_file.run_experiment_encoder, open('encoder.pkl', 'wb'))
        print("Data encoder saved in encoder.pkl file")

    # Save dataset
    tpot_data.to_csv('prepared_data.csv', index=False)
    print('Data saved in prepared_data.csv file')

    # Save target encoder
    if globals_file.run_experiment_target_encoder_used:
        pickle.dump(globals_file.run_experiment_target_encoder, open('target_encoder.pkl', 'wb'))
        print("Target encoder saved in target_encoder.pkl file")

def generate_app_script(data_path='', encoder_path='', target_encoder_path='', app_title='App deployed by AI-Starter'):    
    requirements = """pip-upgrader
pandas
requests
pickle-mixin
scikit-learn
streamlit
feature-engine
    """

    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print('Generated requirements.txt file')


    with open("best_pipeline.py", "r") as txt_file:
        script = txt_file.readlines()

    script = open("best_pipeline.py").read()
    script = script.replace('import numpy as np', '')
    script = script.replace('import pandas as pd', '')
    script = script.replace("'/content\\data_file.csv\', sep=\'COLUMN_SEPARATOR\', dtype=np.float64", "'prepared_data.csv'")
    script = script.replace("results = exported_pipeline.predict(testing_features)", "")

    #code of app.py
    app_script = """import streamlit as st
import pickle
from io import BytesIO
import requests
import pandas as pd 


# Code from Best Pipeline.py here

best_pipeline

######################

# User defined values

title = 'title of the app'
encoder_location = 'encoder.pkl'
target_encoder_location = 'target_encode.pkl'

if len(encoder_location) > 5:
    mfile = BytesIO(requests.get(encoder_location).content)
    encoder = pickle.load(mfile)
    df = encoder.inverse_transform(features)
else:
    df = features.copy()

if len(target_encoder_location) > 5:
    mfile = BytesIO(requests.get(target_encoder_location).content)
    target_encoder = pickle.load(mfile)

st.title(title)

st.sidebar.header('User Input Parameters')

st.subheader('User Input parameters')

selected_data = dict()
for column in df.columns:
    if column != 'target':
        label = column.replace('_id.','')
        label = label.replace('_',' ').title()
        if df[column].dtype == 'O':
            selected_value = st.sidebar.selectbox(label, list(df[column].unique()))
        elif df[column].dtype == 'int64':
            selected_value = st.sidebar.number_input(label, min_value=df[column].min(), max_value=df[column].max(), value=df[column].iloc[0], step=1)

        elif df[column].dtype == 'float64':
            selected_value = st.sidebar.number_input(label, min_value=df[column].min(), max_value=df[column].max(), value=df[column].iloc[0])
        
        selected_data[column] = selected_value

test_data = pd.DataFrame(selected_data, index=[0])

st.write(test_data)

st.subheader('Prediction')
if len(encoder_location) > 5:
    test_data = encoder.transform(test_data) 

prediction = exported_pipeline.predict(test_data)

if len(target_encoder_location) > 5:
    prediction = target_encoder.inverse_transform(prediction)

if 'float' in str(type(prediction[0])):
    st.write(round(prediction[0],2))
else:
    st.write(prediction[0])
    """

    app_script = app_script.replace('best_pipeline', script)
    app_script = app_script.replace('encoder.pkl', encoder_path)
    app_script = app_script.replace('target_encode.pkl', target_encoder_path)
    app_script = app_script.replace('title of the app', app_title)
    app_script = app_script.replace('prepared_data.csv', data_path)


    with open('app.py', 'w') as f:
        f.write(app_script)
    print('Generated app.py file to build the application')
