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

# Create an instance of the LastFmAPI
lastfm_api = LastFmAPI(api_key)

# Example query execution
# query = "INSERT INTO Users (username, country) VALUES ('John', 'john@example.com')"
# db_connector.execute_query(query)
# db_connector.commit_changes()

usernames = ['Robert', 'Chris', 'Lopes', 'Lia', 'Nicole', 'RJ']
count = len(usernames)

while count > 0:
    user_info = lastfm_api.get_user_info(usernames[count-1])

    if user_info is not None:
        name = user_info['user']['name']
        country = user_info['user']['country']
        query = f"INSERT INTO Users (username, country) VALUES ('{name}', '{country}')"
        db_connector.execute_query(query)
        db_connector.commit_changes()
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
