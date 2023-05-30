import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class arima:
    def execute():
            # Read the data from the CSV file
            df = pd.read_csv('file_series.csv')  # Replace 'file.csv' with the actual file name

            # Convert the date column to a pandas datetime object
            df['date'] = pd.to_datetime(df['date'])  # Replace 'date' with the actual column name

            # Set the date column as the DataFrame index
            df.set_index('date', inplace=True)

            # Split the data into training and testing sets
            train_data, test_data = train_test_split(df, test_size=0.26, shuffle=False)  # Adjust the test_size as per your requirement

            # Get the lowest value from the training set
            lowest_value = train_data['values'].min()  # Replace 'column_name' with the actual column name

            # Train the ARIMA model on the training data
            model = ARIMA(train_data['values'], order=(1, 0, 0))  # Replace 'column_name' with the actual column name
            model_fit = model.fit()

            # Predict the lowest value for the next day
            prediction = model_fit.predict(start=len(train_data), end=len(train_data), typ='levels')

            # Evaluate the model on the testing data using MAE
            test_predictions = model_fit.predict(start=len(train_data), end=len(train_data)+len(test_data)-1, typ='levels')
            mae = np.mean(np.abs(test_predictions - test_data['values']))  # Replace 'column_name' with the actual column name

            # Print the predicted lowest value and MAE
            print("Predicted lowest value for the next day:", prediction[0])
            print("Mean Absolute Error (MAE):", mae)

            # Create a plot to visualize the actual and predicted lowest values
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df['values'], label='Actual')
            plt.plot(test_data.index, test_predictions, label='Predicted')
            plt.axhline(y=lowest_value, color='r', linestyle='--', label='Actual Lowest Value')
            plt.title('ARIMA Model - Lowest Value Prediction')
            plt.xlabel('Date')
            plt.ylabel('Lowest Value')
            plt.legend()
            plt.grid(True)

            # Show the plot
            plt.show()