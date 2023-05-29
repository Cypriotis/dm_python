from db_connect import DatabaseConnector
from lastfm_api import LastFmAPI
import pandas as pd
from manageData import manageMissingCells, manageDuplicateInputs , manageOutlierInputs

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


#debug action
db_connector.execute_query('''DROP TABLE Users''')

#db_connector.execute_query('''DROP TABLE Artists''')

db_connector.execute_query('''DROP TABLE Albums''')

db_connector.execute_query('''DROP TABLE UsersFavInfo''')
#creating tables if not exists
db_connector.execute_query('''CREATE TABLE IF NOT EXISTS Users (user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(254), country VARCHAR(254), favorite_artist VARCHAR(254))''')

db_connector.execute_query('''CREATE TABLE IF NOT EXISTS Artists (artists_name VARCHAR(254),mbid VARCHAR(254),artist_url VARCHAR(254))''')

db_connector.execute_query('''CREATE TABLE IF NOT EXISTS Albums(artists_name VARCHAR(254),album_name VARCHAR(254))''')

db_connector.execute_query('''CREATE TABLE IF NOT EXISTS UsersFavInfo (user_name VARCHAR(254),artists_name VARCHAR(254),album_name VARCHAR(254))''')

db_connector.commit_changes()


# Create an instance of the LastFmAPI
lastfm_api = LastFmAPI(api_key)


usernames = ['Robert', 'Chris', 'Lopes', 'Lia', 'Nicole', 'RJ']
count = len(usernames)

while count > 0:
        current_name = usernames[count-1]
        user_info = lastfm_api.get_user_info(current_name)
        user_top_artists = lastfm_api.get_user_top_artists(current_name)

        top_artists = user_top_artists['topartists']['artist']

        name = user_info['user']['name']
        country = user_info['user']['country']
        artist_name = top_artists[0]['name']
        mbid = top_artists[0]['mbid']
        artist_url = top_artists[0]['url']

        query = f"INSERT INTO Artists (artists_name, mbid,artist_url) VALUES ('{artist_name}','{mbid}','{artist_url}')"
        query2 = f"INSERT INTO Users (username, country , favorite_artist) VALUES ('{name}', '{country}' , '{artist_name}')"

        db_connector.execute_query(query)
        db_connector.execute_query(query2)
        db_connector.commit_changes()

        flag = 4
        
        for artist in top_artists:
            flag -= 1
            artist_name = artist['name']
            artists_albums = lastfm_api.get_artists_top_albums(artist_name)
            if(flag>0):
             album_name = artists_albums['topalbums']['album'][flag]['name']
             query = f"INSERT INTO UsersFavInfo (user_name , artists_name, album_name) VALUES ('{current_name}', '{artist_name}', '{album_name}')"
             query2 = f"INSERT INTO Albums (artists_name ,album_name ) VALUES ('{artist_name}','{album_name}')"
             db_connector.execute_query(query)
             db_connector.execute_query(query2)
             db_connector.commit_changes()

        count -= 1

print("We here")

#Execute the following function with the table name as parameter to manage possible missing cells on database
manageMissingCells.execute("Artists")
#Execute the following function with the table name as parameter + the column name to manage the duplicate values on the certain column 
manageDuplicateInputs.execute("Artists","mbid")
#Execute the following function with the table name as parameter + the column name to manage outlier/paranormal values on a certain column
#manageOutlierInputs.execute("Users", "user_id") #doesnt seem to have reason to execute in the current project(may change my mind later)







