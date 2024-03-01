from dotenv import load_dotenv
import os
import sys
import requests

load_dotenv()

#gui = graphics.GUI()

REDIRECT_URI="http://localhost:3000"
API_BASE_URL="https://api.spotify.com/v1/"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

access_parameters = {
    "grant_type" : "client_credentials",
    "client_id" : os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret" : os.getenv("SPOTIFY_CLIENT_SECRET")
}

authorization_dict = {
    "Authorization" : f"Bearer {os.getenv('SPOTIFY_BEARER_TOKEN')}"
}

def get_access():
    r = requests.post(TOKEN_URL, headers={"Content-Type" : "application/x-www-form-urlencoded"}, params=access_parameters)
    data = r.json()
    return data

def refresh_token():
    pass

def search_artist(artist_name:str):
    query = API_BASE_URL + "search" + f"?q={artist_name}&type=artist"
    r = requests.get(query, headers=authorization_dict)
    return r.json()



def get_discography(artist_id:str, release_type:str="album"):
    query = API_BASE_URL + "artists" + f"/{artist_id}" + f"/albums" + f"?include_groups={release_type}&market=US"
    r = requests.get(query, headers=authorization_dict)
    data = r.json()
    release_list = []
    for release in data['items']:
        release_list.append((release['id'], release['name'], release['total_tracks'], release['release_date'], release['album_group']))
    return release_list



if __name__=="__main__":
    print("Running \"spotify_requests.py\" is reserved for testing.")