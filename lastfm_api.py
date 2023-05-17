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
            return None