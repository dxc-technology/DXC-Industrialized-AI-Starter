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
