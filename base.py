from db_connect import DatabaseConnector
from lastfm_api import LastFmAPI
import pandas as pd
from manageData import manageMissingCells, manageDuplicateInputs, manageOutlierInputs, exportStatistics, trendSpotter
from arima import arima
from database_init import database_init
from helperAI import chatgpt
from nameFiltering import filter
from recommend import recommend
import random
from generateRandomLatLon import generate_synthetic_locations


# MySQL database connection details
host = 'localhost'
username = 'root'
password = ''
database = 'DeMa'
port = '3308'

# Last.fm API key
api_key = '899c27976ecfa7b4adf9f276b445d62f'

# Create an instance of the DatabaseConnector
db_connector = DatabaseConnector(host, username, password, database, port)
db_connector.connect()

# initializing the tables of the database
database_init.execute()

# Have a problem with api call limit. Hold for now
# chatgpt.execute()

# Filter random users engine with users that actually exists on last fm database
filter.execute()
# managing duplicate generated names
manageDuplicateInputs.execute("Filtered", "name")


# Create an instance of the LastFmAPI
lastfm_api = LastFmAPI(api_key)


# usernames = ['Robert', 'Mayia', 'Lopes', 'Lia', 'Nicole', 'RJ','Weston','Fae','Twila']


# Retrieve names from the database
query = "SELECT name FROM Filtered"
db_connector.execute_query(query)

# Fetch all rows and store the values in a list
usernames = [row[0] for row in db_connector.fetchall()]

count = len(usernames)

while count > 0:
    current_name = usernames[count-1]
    user_info = lastfm_api.get_user_info(current_name)
    user_top_artists = lastfm_api.get_user_top_artists(current_name)
    user_top_tracks = lastfm_api.get_user_top_songs(current_name)

    top_artists = user_top_artists['topartists']['artist']
    # Extract song information from the API response
    tracks = user_top_tracks['lovedtracks']['track']

    name = user_info['user']['name']
    country = user_info['user']['country']
    artist_name = top_artists[0]['name']
    playcount = top_artists[0]['playcount']
    mbid = top_artists[0]['mbid']
    artist_url = top_artists[0]['url']

    ##Generate random lat lot for user and their 3 loved songs generate_synthetic_locations(number of pairs to generate, max distance from each other)
    locations=generate_synthetic_locations(4, 1000)
    print(locations[0][0])


    # Cleaning unacceptable characters for MariaDB like '
    helper = ""
    for x in range(3):
        helper = tracks[x]['name']
        size = len(helper)
        new_string = helper.replace("'", "B")
        tracks[x]['name'] = new_string

    query = f"INSERT INTO UserSongs (user_name , song_name,song_name2,song_name3) VALUES ('{name}', '{tracks[0]['name']}','{tracks[1]['name']}','{tracks[2]['name']}')"
    db_connector.execute_query(query)
    db_connector.commit_changes()

    query = f"INSERT INTO LatLon (name, lat, lon, song1, song1_lat, song1_lon, song2, song2_lat, song2_lon, song3, song3_lat, song3_lon) VALUES ('{name}','{locations[0][0][0]}','{locations[0][0][1]}', '{tracks[0]['name']}','{locations[0][1][0]}','{locations[0][1][1]}','{tracks[1]['name']}','{locations[0][2][0]}','{locations[0][2][1]}','{tracks[2]['name']}','{locations[0][3][0]}','{locations[0][3][1]}')"
    db_connector.execute_query(query)
    db_connector.commit_changes()


    query = f"INSERT INTO Artists (artists_name, mbid,artist_url) VALUES ('{artist_name}','{mbid}','{artist_url}')"
    query2 = f"INSERT INTO Users (username, country , favorite_artist, playcount) VALUES ('{name}', '{country}' , '{artist_name}','{playcount}')"
    
    db_connector.execute_query(query)
    db_connector.execute_query(query2)
    db_connector.commit_changes()

    flag = 4

    for artist in top_artists:
        flag -= 1
        artist_name = artist['name']
        artists_albums = lastfm_api.get_artists_top_albums(artist_name)
        if (flag > 0):
            album_name = artists_albums['topalbums']['album'][flag]['name']
            helper = album_name
            new_string = helper.replace("'", "B")
            album_name = new_string
            query = f"INSERT INTO UsersFavInfo (user_name , artists_name, album_name) VALUES ('{current_name}', '{artist_name}', '{album_name}')"
            query2 = f"INSERT INTO Albums (artists_name ,album_name ) VALUES ('{artist_name}','{album_name}')"
            db_connector.execute_query(query)
            db_connector.execute_query(query2)
            db_connector.commit_changes()

    count -= 1

print("We here")

# Execute the following function with the table name as parameter to manage possible missing cells on database
manageMissingCells.execute("Artists")
# Execute the following function with the table name as parameter + the column name to manage the duplicate values on the certain column
manageDuplicateInputs.execute("UserSongs", "user_name")
# Execute the following function with the table name as parameter + the column name to manage outlier/paranormal values on a certain column
# manageOutlierInputs.execute("Users", "user_id") #doesnt seem to have reason to execute in the current project(may change my mind later)

exportStatistics.execute("Users", "playcount")

trendSpotter.execute()

arima.execute()

recommend.execute()

