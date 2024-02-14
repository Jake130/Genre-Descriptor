from dotenv import load_dotenv
import os
import sys
import requests

load_dotenv()

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

def search_artist(artist_name:str):
    query = API_BASE_URL + "search" + f"?q={artist_name}&type=artist"
    r = requests.get(query, headers=authorization_dict)
    return r.json()

def reprompt_searched_artist(search_json, index):
    if index>=search_json['artists']['total']:
        print("There are no other artists under this name... quitting program")
        sys.exit()
    this_artist = search_json['artists']['items'][index]
    print("Is the artist you're looking for: " + this_artist['name'] + "?")
    #Print all artist's genres and followers
    res = f"Followers: {this_artist['followers']['total']}"
    if this_artist['genres']!=[]:
        res += "\tKnown Genres: "
        for genre in this_artist['genres']:
            res += genre + ", "
    print(res)

    print("Enter 'no' if this is not the case")
    input = sys.stdin.readline()
    if input.lower()=="no\n":
        return True
    return False

def display_profile():
    pass


def get_discography(artist_id:str, release_type:str="album"):
    query = API_BASE_URL + "artists" + f"/{artist_id}" + f"/albums" + f"?include_groups={release_type}&market=US"
    r = requests.get(query, headers=authorization_dict)
    data = r.json()
    release_list = []
    for release in data['items']:
        release_list.append((release['id'], release['name'], release['total_tracks'], release['release_date'], release['album_group']))
    return release_list



if __name__=="__main__":
    arguments = sys.argv
    if len(sys.argv)<3:
        raise RuntimeError("There are too little arguments!")
    if len(sys.argv)>5:
        raise RuntimeError("More than four arguments were entered!")
    #Allow the user to search for the artist they're looking for
    print(get_access())
    searched_artist = search_artist(arguments[1])
    index = 0
    while True:
        response = reprompt_searched_artist(searched_artist, index)
        index += 1
        if response==False:
            break
    index -= 1
    selected_artist = searched_artist['artists']['items'][index]['id']
    #Make album list from Spotify API
    album_list = get_discography(selected_artist)
    print(album_list)