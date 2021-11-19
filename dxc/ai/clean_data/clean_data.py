import pandas as pd
import janitor #data cleaning
from ftfy import fix_text #data cleaning
import nltk #data cleaning
nltk.download('punkt') #data cleaning
import scrubadub #data cleaning
import arrow #normalizing dates
import numpy as np
from sklearn.base import TransformerMixin
from dxc.ai.global_variables import globals_file


class DataFrameImputer(TransformerMixin):
    def __init__(self):
        """Impute missing values.
        Columns of dtype object are imputed with the most frequent value 
        in column.
        Columns of other types are imputed with mean of column.
        """
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

#CLEANING FILE

def clean_dataframe(df, impute = False, text_fields = [], date_fields = [], numeric_fields = [], categorical_fields = []):

    clean_df = (
      df
      #make the column names lower case and remove spaces
      .clean_names()

      #remove empty columns
      .remove_empty()

      #remove empty rows and columns
      .dropna(how='all')
    )

    #remove harmful characters. remove personal identifiers. make lowercase
    for field in text_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = clean_df[field].fillna(' ').apply(fix_text)
        clean_df[field] = clean_df[field].apply(scrubadub.clean, replace_with='identifier')
        clean_df[field] = clean_df[field].str.lower()
  
    #impute missing values
    if impute:
        clean_df = DataFrameImputer().fit_transform(clean_df)

    #standardize the format of all date fields
    for field in date_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = clean_df[field].apply(arrow.get)

    #make sure all numeric fields have the proper data type
    for field in numeric_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = pd.to_numeric(clean_df[field])
  
    #make sure all categorical variables have the proper data type
    for field in categorical_fields:
        field = '_'.join(field.split()).lower()
        clean_df[field] = clean_df[field].astype('category')
    
    clean_df=clean_df.clean_names()
    
    globals_file.clean_data_used = True

    return(clean_df)
