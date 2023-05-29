from db_connect import DatabaseConnector
from lastfm_api import LastFmAPI

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

db_connector.execute_query('''DROP TABLE Artists''')

db_connector.execute_query('''DROP TABLE Albums''')

db_connector.execute_query('''DROP TABLE UsersFavInfo''')
#creating tables if not exists
db_connector.execute_query('''CREATE TABLE IF NOT EXISTS Users (user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(254), country VARCHAR(254), favorite_artist VARCHAR(254))''')

db_connector.execute_query('''CREATE TABLE IF NOT EXISTS Artists (artists_name VARCHAR(254),mbid VARCHAR(254),artists_url VARCHAR(254))''')

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
        print(current_name)
        country = user_info['user']['country']
        artist_name = top_artists[0]['name']
        query = f"INSERT INTO Users (username, country , favorite_artist) VALUES ('{name}', '{country}' , '{artist_name}')"
        db_connector.execute_query(query)
        db_connector.commit_changes()
        flag = 4
        for artist in top_artists:
            flag -= 1
            artist_name = artist['name']
            artists_albums = lastfm_api.get_artists_top_albums(artist_name)
            if(flag>0):
             album_name = artists_albums['topalbums']['album'][flag]['name']
             query = f"INSERT INTO UsersFavInfo (user_name , artists_name, album_name) VALUES ('{current_name}', '{artist_name}', '{album_name}')"
             db_connector.execute_query(query)
             db_connector.commit_changes()
             print(album_name)

        count -= 1

count = len(usernames)
artists_sum = 0
artists_names = []
while count > 0:
    user_top_artists = lastfm_api.get_user_top_artists(usernames[count-1])

    top_artists = user_top_artists['topartists']['artist']

    for artist in top_artists:
        artists_sum += 1
        artist_id = artist['mbid']
        artist_name = artist['name']
        artists_names.append(artist_name)
        print('A , B : ', artist_id, artist_name )
        query = f"INSERT INTO MusicGroups (group_id, group_name) VALUES ('{artist_id}', '{artist_name}')"
        db_connector.execute_query(query)
        db_connector.commit_changes()
    count -= 1

##count = 6
while count > 0:
    artists_albums = lastfm_api.get_artists_top_albums(artists_names.pop(1))

    top_albums = artists_albums['topalbums']['album']
    print("HERE : " ,top_albums)

     # Iterate over the top albums
    #for album in top_albums:
    #    album_name = album['name']
    #    artist_name = album['artist']['name']
    #    print('A , B : ', album_name, artist_name)
    #    query = f"INSERT INTO Albums (album_name, artist_name) VALUES ('{album_name}', '{artist_name}')"
    #    db_connector.execute_query(query)
    #    db_connector.commit_changes()
    #count -= 1


# Disconnect from the databas
