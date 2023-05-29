import pandas as pd
from sqlalchemy import create_engine


class manageMissingCells:
    def execute(t_name): # Connection details
        host = 'localhost'
        user = 'root'
        password = ''
        database = 'DeMa'
        port = '3308'

        # MySQL connection URL
        url = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'

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
        def tesT(): 
             print("Missing Implementation")


class manageOutlierInputs:
        def tesT(): 
             print("Missing Implementation")