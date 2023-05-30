import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os
from datetime import date
from statsmodels.tsa.seasonal import seasonal_decompose


host = 'localhost'
user = 'root'
password = ''
database = 'DeMa'
port = '3308'

# MySQL connection URL
url = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'


class manageMissingCells:
    def execute(t_name): # Connection details
        

        # Retrieve data from the database into a pandas DataFrame
        query = 'SELECT * FROM '
        query += t_name
        engine = create_engine(url)
        df = pd.read_sql_query(query, engine)

        # Replace empty cells with NULL values in the DataFrame
        df = df.replace('', pd.NA)

        # Write the modified DataFrame back to the database
        df.to_sql(t_name, engine, if_exists='replace', index=False)

        # Close the database connection
        engine.dispose()



class manageDuplicateInputs:
        def execute(t_name,col1): 
            # Create the SQLAlchemy engine
            engine = create_engine(url)

            # Retrieve data from the database into a pandas DataFrame
            query = 'SELECT * FROM '
            query += t_name
            df = pd.read_sql_query(query, engine)

            # Drop duplicates based on specified columns
            columns_to_check_duplicates = [col1]  # Replace with the actual column names
            df.drop_duplicates(subset=columns_to_check_duplicates, inplace=True)

            # Write the modified DataFrame back to the database
            df.to_sql(t_name, engine, if_exists='replace', index=False)

            # Close the database connection
            engine.dispose()

class manageOutlierInputs:
        def execute(t_name,col1): 
             # Create the SQLAlchemy engine
            engine = create_engine(url)

            # Retrieve data from the database into a pandas DataFrame
            query = 'SELECT * FROM '
            query += t_name
            df = pd.read_sql_query(query, engine)

            # Identify and handle outliers
            column_name = col1  # Replace with the actual column name
            lower_bound = 0  # Replace with the lower bound value for outliers
            upper_bound = 5  # Replace with the upper bound value for outliers

            # Replace outliers with null values
            df.loc[(df[col1] < lower_bound) | (df[col1] > upper_bound), col1] = None

            # Write the modified DataFrame back to the database
            df.to_sql(t_name, engine, if_exists='replace', index=False)

            # Close the database connection
            engine.dispose()

class exportStatistics:
        def execute(t_name,col1):
               # Create the engine with the connection URL
                engine = create_engine(url)

                # Write a SQL query to retrieve the data from the database
                query = "SELECT * FROM "
                query += t_name

                # Use pd.read_sql() to execute the query and store the data in a DataFrame
                df = pd.read_sql(query, engine)

                # Perform summary statistics calculations on the DataFrame
                mean = df[col1].mean()
                median = df[col1].median()
                std_dev = df[col1].std()
                min_value = df[col1].min()
                max_value = df[col1].max()

                # Print or use the calculated summary statistics as desired
                print("Mean:", mean)
                print("Median:", median)
                print("Standard Deviation:", std_dev)
                print("Minimum Value:", min_value)
                print("Maximum Value:", max_value)

                # Visualize the data using a histogram
                plt.hist(df[col1], bins=10)
                plt.xlabel('Value')
                plt.ylabel('Frequency')
                plt.title('Histogram of '+col1)

                # Visualize the data using a box plot
                plt.boxplot(df[col1])
                plt.ylabel('Value')
                plt.title('Box Plot of '+ col1)

                # Create a directory to save the plots if it doesn't exist
                output_dir = 'plots'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Create a pie chart
                labels = ['Below Average', 'Average', 'Above Average']
                values = [
                    len(df[df[col1] < mean]),
                    len(df[df[col1] == mean]),
                    len(df[df[col1] > mean])
                ]
                plt.pie(values, labels=labels, autopct='%1.1f%%')
                plt.title('Distribution of Values')


                # Get the current date
                current_date = date.today().strftime("%Y-%m-%d")

                # Save the pie chart with the current date in the file name
                file_name = f'pie_chart_{current_date}.png'
                plt.savefig(os.path.join(output_dir, file_name))

                # Close the connection
                engine.dispose()         
class trendSpotter:
      def execute():
                # Read the data from the CSV file
                df = pd.read_csv('file_series.csv')

                # Convert the date column to a pandas datetime object
                df['date'] = pd.to_datetime(df['date'])  # Replace 'date' with the actual column name

                # Set the date column as the DataFrame index
                df.set_index('date', inplace=True)

                # Perform the decomposition
                result = seasonal_decompose(df['values'], model='additive')

                # Access the decomposed components
                trend = result.trend
                seasonality = result.seasonal
                residuals = result.resid

                # Specify the export directory path
                export_dir = 'sythetic'

                # Create the export directory if it doesn't exist
                if not os.path.exists(export_dir):
                    os.makedirs(export_dir)

                # Export the decomposed components to separate CSV files
                trend.to_csv(os.path.join(export_dir, 'trend.csv'), index=True)
                seasonality.to_csv(os.path.join(export_dir, 'seasonality.csv'), index=True)
                residuals.to_csv(os.path.join(export_dir, 'residuals.csv'), index=True)

                # Set the sampling interval
                sampling_interval = 7  # Change the value as per your desired sampling frequency

                # Sample the data
                sampled_df = df[::sampling_interval]
                sampled_seasonality = seasonality[::sampling_interval]
                sampled_residuals = residuals[::sampling_interval]

                # Increase the figure size
                plt.figure(figsize=(12, 8))  # Adjust the values as needed

                # Plot the trend
                plt.subplot(3, 1, 1)
                plt.plot(sampled_df.index, sampled_df['values'])
                plt.title('Trend')

                # Plot the seasonality
                plt.subplot(3, 1, 2)
                plt.scatter(sampled_seasonality.index, sampled_seasonality, s=100)
                plt.title('Seasonality')

                # Plot the residuals
                plt.subplot(3, 1, 3)
                plt.plot(sampled_residuals.index, sampled_residuals)
                plt.title('Residuals')

                # Adjust the spacing between subplots
                plt.tight_layout()

                # Save the plot in the export directory
                plt.savefig(os.path.join(export_dir, 'synthetic_data_set.png'))

                # Display the plot
                plt.show()