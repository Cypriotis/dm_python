from db_connect import DatabaseConnector
from lastfm_api import LastFmAPI

# MySQL database connection details
host = 'localhost'
username = 'root'
password = ''
database = 'dmpython'
port = '3307'

# Last.fm API key
api_key = '899c27976ecfa7b4adf9f276b445d62f'

# Create an instance of the DatabaseConnector
db_connector = DatabaseConnector(host, username, password, database ,port)
db_connector.connect()

# Create an instance of the LastFmAPI
lastfm_api = LastFmAPI(api_key)

# Example query execution
query = "INSERT INTO Users (username, country) VALUES ('John', 'john@example.com')"
db_connector.execute_query(query)
db_connector.commit_changes()

# Example Last.fm API usage
username = 'some_user'
user_info = lastfm_api.get_user_info(username)

# Store the user info in the database
if user_info is not None:
    name = user_info['user']['name']
    country = user_info['user']['country']
    query = f"INSERT INTO Users (username, country) VALUES ('{name}', '{country}')"
    db_connector.execute_query(query)
    db_connector.commit_changes()

# Disconnect from the databas