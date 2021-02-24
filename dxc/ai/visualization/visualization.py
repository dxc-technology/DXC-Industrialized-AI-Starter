#VISUALIZATION
from yellowbrick.features import Rank2D #exploring raw data
import matplotlib.pyplot as plt
import missingno as msno #gauge dataset completeness
import seaborn as sns #data exploration, distribution plotting
import pandas as pd
from datacleaner import autoclean
import math
from pandas.api.types import is_numeric_dtype
from pandas_profiling import ProfileReport


#VISUALIZATION

#display the correlations in pairwise comparisons of all features
def explore_features(df):
    df_copy = df.copy()

    #for some reason, the visualize doesn't accept categorical
    #variables. those have to be converted to strings
    for (col,data) in df_copy.iteritems():
        if df_copy[col].dtype.name == "category":
            df_copy[col] = df_copy[col].astype(str)

    numeric_df = autoclean(df_copy)
    visualizer = Rank2D(algorithm="pearson")
    visualizer.fit_transform(numeric_df)
    visualizer.poof()

#display a visual representation of missing fields in the given data
def visualize_missing_data(df):
    msno.matrix(df, figsize=(15,8))
    
def explore_complete_data(df, title='Complete Data Report'):
    profile = ProfileReport(df, title, html={'style':{'full_width':False}})
    return profile

#plot the distribution of values of each field in the given data
def plot_distributions(df):

    #set plot style
    sns.set(style="darkgrid")

    features = len(df.columns)

    #determine the number of columns in the plot grid and the width and height of each plot
    grid_cols = 3
    plot_width = 5
    plot_height = 3

    #determine the width of the plot grid and number of rows
    grid_width = plot_width * grid_cols
    num_rows = math.ceil(features/grid_cols)

    #determine the width of the plot grid
    grid_height = plot_height * num_rows

    #lay out the plot grid
    fig1 = plt.figure(constrained_layout=True, figsize = (grid_width,grid_height))
    gs = fig1.add_gridspec(ncols = grid_cols, nrows = num_rows)

    #step through the dataframe and add plots for each feature
    current_column = 0
    current_row = 0
    for col in df.columns:

        #set up a plot
        f1_ax1 = fig1.add_subplot(gs[current_row, current_column])
        f1_ax1.set_title(col)

        #create a plot for numeric values
        if is_numeric_dtype(df[col]):
            sns.histplot(df[col], ax = f1_ax1, kde = True).set_xlabel('')
    
        #creare a plot for categorical values
        if df[col].dtype.name == "category":
            sns.countplot(df[col], ax = f1_ax1, order = df[col].value_counts().index).set_xlabel('')

        #move to the next column
        current_column +=1

        #determine if it is time to start a new row
        if current_column == grid_cols:
            current_column = 0
            current_row +=1
