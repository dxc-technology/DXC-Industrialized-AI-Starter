# import numpy as np
# import pandas as pd
# import operator
# import plotly
# import sys
# import datetime
# from collections import defaultdict, Counter
# from matplotlib import pyplot as plt
# #%matplotlib inline

# from statsmodels.tsa.stattools import adfuller
# from statsmodels.tsa.seasonal import seasonal_decompose
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from sklearn.metrics import mean_squared_error
# from statsmodels.tsa.ar_model import AR
# from statsmodels.tsa.arima_model import ARMA, ARIMA
# from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing

# import pyaf.ForecastEngine as autof

# from pmdarima.arima import auto_arima
# from pmdarima.model_selection import train_test_split

# import warnings
# warnings.filterwarnings('ignore', 'statsmodels.tsa.ar_model.AR', FutureWarning)


# #Dickey-Fuller Test for stationary check
# def adf_test(timeseries):
#     #Perform Dickey-Fuller test:
#     print('Results of Augmented Dickey-Fuller(ADF) Statistical Test:')
#     dftest = adfuller(timeseries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
#     for key,value in dftest[4].items():
#        dfoutput['Critical Value (%s)'%key] = value
#     print(dfoutput)

# #autoRegressiveModel
# def autoRegressiveModel(df, no_predictions = 7, debug = False , visualize = False):
#     data = df.values
#     # Splitting data into train and test set.
#     train, test = data[1:len(data)-no_predictions], data[len(data)-no_predictions:]
#     # train autoregression
#     model = AR(train)
#     model_fit = model.fit()
#     if(debug):
#         print(model_fit.summary())
#     # make predictions
#     predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1+no_predictions, dynamic=False)
#     if(visualize):
#         plt.plot(test , color = "blue" , label = "testing data")
#         plt.plot(predictions, color='red' , label = "prediction")
#         plt.legend(loc='best')
#         plt.show()
#     error = np.sqrt(mean_squared_error(test, predictions[:no_predictions]))
#     return (predictions[-no_predictions:] , error, model_fit)

# def simpleExponentialSmoothing(df, no_predictions=7, debug = False , visualize = False):
#     train_data, test_data = df[1:int(len(df)-no_predictions)], df[int(len(df)-no_predictions):]
#     fit1 = SimpleExpSmoothing(np.asarray(train_data)).fit(smoothing_level=0.85 , optimized=False)
#     if(debug):
#          print(fit1.summary())
#     predictions = fit1.forecast(no_predictions*2)
#     if(visualize):
#         plt.plot(list(test_data), color = 'blue', label='testing data')
#         plt.plot(list(predictions), color = 'red',label='prediction')
#         plt.legend(loc='upper left', fontsize=8)
#         plt.show()
#     error = np.sqrt(mean_squared_error(test_data, predictions[:no_predictions]))
#     return (predictions[-no_predictions:] , error, fit1)

# def doubleSmoothing(df, no_predictions=7, debug = False , visualize = False):
#     train_data, test_data = df[1:int(len(df)-no_predictions)], df[int(len(df)-no_predictions):]
#     model = ExponentialSmoothing(np.asarray(train_data), trend='add', seasonal=None)
#     fit1 = model.fit()
#     if(debug):
#         print(fit1.summary())
#     predictions = fit1.forecast(no_predictions*2)
#     if(visualize):
#         plt.plot(list(test_data), color = 'blue', label='testing data')
#         plt.plot(list(predictions), color = 'red',label='prediction')
#         plt.legend(loc='upper left', fontsize=8)
#         plt.show()
#     error = np.sqrt(mean_squared_error(test_data, predictions[:no_predictions]))
#     return (predictions[-no_predictions:] , error, fit1)


# def autoRegressiveMovingAverageModel(df, order=(1,0), no_predictions=7, debug=False , visualize=False):
#     data = df.values
#     train, test = data[1:len(data)-no_predictions], data[len(data)-no_predictions:]
#     model = ARMA(train, order = order)
#     model_fit = model.fit()
#     if(debug):
#         print(model_fit.summary())
#     predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1+no_predictions, dynamic=False)
#     if(visualize):
#         plt.plot(test , color = "blue" , label = "testing data")
#         plt.plot(predictions, color='red' , label = "prediction")
#         plt.legend(loc='best')
#         plt.show()
#     error = np.sqrt(mean_squared_error(test, predictions[:no_predictions]))
#     return (predictions[-no_predictions:] , error, model_fit)

# def getBestForcastingModel(df, no_predictions=7, debug=False, visualize = False):
#     modelResults = {}
#     modelResults["autoRegressiveModel"] = autoRegressiveModel(df, no_predictions)[1]
#     modelResults["simpleExponentialSmoothing"] = simpleExponentialSmoothing(df, no_predictions)[1]
#     modelResults["doubleSmoothing"] = doubleSmoothing(df, no_predictions)[1]
#     modelResults["autoRegressiveMovingAverageModel"] = autoRegressiveMovingAverageModel(df, order=(1,0), no_predictions=no_predictions)[1]
#     bestModel = min(modelResults.items(), key=operator.itemgetter(1))[0]
#     print(bestModel)
#     print(adf_test(df))
#     if bestModel == 'autoRegressiveModel':
#         results, error, model = autoRegressiveModel(df, no_predictions, debug, visualize)
#         print('RMSE:', error)
#         return model
#     elif bestModel == 'simpleExponentialSmoothing':
#         results, error, model =  simpleExponentialSmoothing(df, no_predictions, debug, visualize)
#         print('RMSE:', error)
#         return model
#     elif bestModel == 'doubleSmoothing':
#         results, error, model = doubleSmoothing(df, no_predictions, debug, visualize)
#         print('RMSE:', error)
#         return model
#     elif bestModel == 'autoRegressiveMovingAverageModel':
#         results, error, model = autoRegressiveMovingAverageModel(df, order=(1,0), no_predictions=no_predictions, debug=debug, visualize=visualize)
#         print('RMSE:', error)
#         return model
