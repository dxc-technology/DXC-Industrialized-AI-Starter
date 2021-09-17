# import numpy as np
# import pandas as pd
# import tensorflow as tf
# import ktrain
# from ktrain import text

# def texts_from_df(train_df,val_df,text_column,label_columns,maxlen = 400,preprocess_mode = 'bert'):
    
#     (X_train,y_train), (X_test,y_test), preprocess = text.texts_from_df(train_df = train_df,
#                                                                     text_column = text_column,
#                                                                     label_columns = label_columns,
#                                                                     val_df = val_df,
#                                                                     maxlen = maxlen,
#                                                                     preprocess_mode = preprocess_mode)
#     return (X_train,y_train), (X_test,y_test), preprocess
    

    
# def get_model_learner(train_data,val_data,preproc,name = 'bert',batch_size=6):
#     model = text.text_classifier(name = name, train_data = train_data,preproc = preproc)
#     learner = ktrain.get_learner(model = model, 
#                              train_data = train_data, 
#                              val_data = val_data, 
#                              batch_size = batch_size)
#     return model, learner


# def get_predictor(learner,preprocess):
#     predictor = ktrain.get_predictor(learner.model, preprocess)
#     return predictor
