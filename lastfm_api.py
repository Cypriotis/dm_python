import requests

class LastFmAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_user_info(self, username):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={self.api_key}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Something went wrong on the request")
            return None
    
    def get_user_top_artists(self, username):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={self.api_key}&limit=5&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Something went wrong on the request")
            return None
    
    def get_artists_top_albums(self, artists_name):
        url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artists_name}&api_key={self.api_key}&limit=4&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Something went wrong on the request")
            return None
    
    def get_user_top_songs(self, username):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={self.api_key}&limit=3&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Something went wrong on the request")
            return None