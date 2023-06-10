import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt


class arima():
    def execute():
        # Read the CSV file
        df = pd.read_csv('file_series.csv', parse_dates=['date'], index_col='date')

        # Split the values into training and testing sets
        train_size = int(len(df) * 0.66)
        train, test = df[:train_size]['values'], df[train_size:]['values']

        # Train the ARIMA model
        history = [x for x in train]
        predictions = []
        for t in range(len(test)):
            model = ARIMA(history, order=(5, 1, 0))
            model_fit = model.fit()
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            print('predicted=%f, expected=%f' % (yhat, obs))

        # Calculate RMSE
        rmse = sqrt(mean_squared_error(test, predictions))
        print('Test RMSE: %.3f' % rmse)

        # Plot the actual values and predictions
        plt.plot(test.index, test, label='Actual')
        plt.plot(test.index, predictions, color='red', label='Predicted')
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title('ARIMA Model - Actual vs Predicted')
        plt.legend()

        # Display the plot
        plt.show()
