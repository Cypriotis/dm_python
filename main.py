import requests
import random
import sqlite3

# Define the base URL for the Last.fm API
base_url = 'http://ws.audioscrobbler.com/2.0/'

# Define your Last.fm API key (replace 'YOUR_API_KEY' with your actual API key)
api_key = '899c27976ecfa7b4adf9f276b445d62f'

# Define the method to get user information
method = 'user.getInfo'


count = 0
# Generate a random Last.fm username or use a predefined list of usernames
# Here, we use a predefined list of usernames for demonstration purposes
usernames = ['Robert', 'Chris', 'Lopes','Lia','Nicole','RJ']




while count <6:
        
        # Connect to the SQLite database
        conn = sqlite3.connect('db1.db')
        cursor = conn.cursor()

        # Create the Users table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    user_id INT PRIMARY KEY,
                    username VARCHAR(50),
                    country VARCHAR(50)
                    )''')
        
        # Create the MusicGroups table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS MusicGroups (
                            group_id VARCHAR(254) PRIMARY KEY,
                            group_name VARCHAR(100)
                            )''')
    
        # Create the Albums table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Albums (
                    album_id VARCHAR(250) PRIMARY KEY,
                    album_name VARCHAR(100),
                    artist_name VARCHAR(200),
                    release_year INT
                    )''')
        
        # Define the parameters for the method
        params = {
          'api_key': api_key,
          'format': 'json',
          'user': usernames[count]
            }
        

        # Make the API call to get user information
        response = requests.get(base_url + '?method=' + method, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the JSON data from the response
            data = response.json()
            
            # Process the user information as needed
            # For example, print the user's name and country
            user = data['user']
            name = user['name']
            country = user['country']
            age = user['age']
            playcount = user['playcount']
            

            print('Name: ', name)
            print('Country: ', country)

                #Insert user information into the Users table
            cursor.execute("INSERT INTO Users (username,country) VALUES (?, ?)",(name,country))
                
                    # Commit the changes after each user insertion
        conn.commit()

        count+=1
           

else:
    if count !=6:
     print('Error making API call. Status code:', response.status_code)
    



# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute a SELECT query to retrieve data
cursor.execute("SELECT * FROM Users")

# Fetch all rows from the result set
rows = cursor.fetchall()

temp = []
users = []

# Iterate over the rows and process the data
for row in rows:
    username = row[1]
    country = row[2]
    temp.append(row[1])
    users.append(row[1])
    #Process the data as needed
    #print("Username:", username)
    #print("Country:", country)
    #print("---------------------------------")

# Define the method to retrieve random users
method = 'user.getRecentTracks'

count = len(temp)


while count !=0:
    username=temp.pop()
    print("WE HERE : " , username)
    params = {
            'api_key': api_key,
            'format': 'json',
            'limit': 1,  # Number of random users to retrieve
            'user': username
        }
    
    response = requests.get(base_url + '?method=' + method, params=params)

    if response.status_code == 200:

         # Extract the JSON data from the response
        data = response.json()
        print(data)
        print('\n')
        print('\n')
        print('\n')
    count -= 1


count = 6
# Define the method to get user's top artists
method = 'user.getTopArtists'

artists = []

while count >= 1:
    username = users.pop()
    # Define the parameters for the method
    params = {
        'api_key': api_key,
        'format': 'json',
        'user': username,
        'period': 'overall',  # Choose the desired period (overall, 7day, 1month, 3month, 6month, 12month)
        'limit': 1  # Number of top artists to retrieve
    }


    # Make the API call to get user's top artists
    response = requests.get(base_url + '?method=' + method, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()

        top_artists = data['topartists']['artist']

        for artist in top_artists:
         artist_id = artist['mbid']
         artist_name = artist['name']
         artists.append(artist_name)

         print('A , B : ', artist_id , artist_name)
        
        # Insert the artist information into the Artists table
        cursor.execute("INSERT INTO MusicGroups (group_id, group_name) VALUES (?, ?)",
                       (artist_id, artist_name))
        
        # Commit the changes to the database
        conn.commit()




    count -= 1

# Define the method to get top albums of an artist
method = 'artist.getTopAlbums'

count = 6

print(artists)
    
while count >= 1:
    artistsTemp = artists.pop()
    # Define the parameters for the method
    params = {
    'api_key': api_key,
    'format': 'json',
    'artist': artistsTemp,
    'limit': 1  # Number of top albums to retrieve
    }   
    count -=1


    # Make the API call to get the top albums of the artist
    response = requests.get(base_url + '?method=' + method, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        top_albums = data['topalbums']['album']

        # Iterate over the top albums
        for album in top_albums:
            album_name = album['name']
            artist_name = album['artist']['name']

            # Insert the album information into the Albums table
            cursor.execute("INSERT INTO Albums (album_name, artist_name) VALUES (?, ?)",
                        (album_name, artistsTemp))

        # Commit the changes to the database
        conn.commit()

        

    else:
        print('Error making API call. Status code:', response.status_code)


# Close the database connection
        conn.close()