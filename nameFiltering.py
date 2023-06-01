from db_connect import DatabaseConnector
from database_init import database_init
from lastfm_api import LastFmAPI
import requests


# MySQL database connection details
host = 'localhost'
username = 'root'
password = ''
database = 'DeMa'
port = '3308'


# Last.fm API endpoint
api_url = "http://ws.audioscrobbler.com/2.0/"

# Last.fm API key
api_key = '899c27976ecfa7b4adf9f276b445d62f'

# Create an instance of the DatabaseConnector
db_connector = DatabaseConnector(host, username, password, database, port)
db_connector.connect()

# Create an instance of the LastFmAPI
lastfm_api = LastFmAPI(api_key)

# Retrieve names from the database
query = "SELECT name FROM Test"
db_connector.execute_query(query)
# Fetch all the names from the result set
names = db_connector.fetch_all_rows()

namess=list(names)






class filter:
    def execute():


        for name in namess:
            # Parameters for user.getLovedTracks request
            loved_tracks_params = {
                "method": "user.getLovedTracks",
                "user": name,
                "api_key": api_key,
                "format": "json",
                "limit": 1,
                "page": 1
            }


            # Make the user.getLovedTracks request
            loved_tracks_response = requests.get(api_url, params=loved_tracks_params)
            loved_tracks_data = loved_tracks_response.json()

            # Try to get the total loved tracks count
            try:
                total_loved_tracks = int(loved_tracks_data["lovedtracks"]["@attr"]["total"])
            except KeyError:
                total_loved_tracks = 0

            if total_loved_tracks > 3:
                # Print the total loved tracks count
                print(f"Total loved tracks for user {username}: {total_loved_tracks}")
                #print(namess[1]["name"])
                #query=f"INSERT INTO Filtered (name) VALUES ('{name}')"
                #db_connector.execute_query(query)
                #db_connector.commit_changes()

            


            #for name in names:
            #    user_top_tracks = lastfm_api.get_user_top_songs(name)
            #    tracks = user_top_tracks['lovedtracks']['@attr']['total']
            #    songs_amount = tracks['lovedtracks']['total']
            #    print(songs_amount)
                