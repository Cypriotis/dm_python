import pandas as pd
from sqlalchemy import create_engine

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
        def tesT(): 
             print("Missing Implementation")