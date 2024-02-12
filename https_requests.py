import requests
import json
from dotenv import load_dotenv
import os
import sys

load_dotenv()

musixmatch_root_URL = "https://api.musixmatch.com/ws/1.1/"
httpbin_base_url = "https://httpbin.org/get" 

CHART_TRACKS_GET = "chart.tracks.get"
CHART_ARTISTS_GET = "chart.artists.get"
ARTIST_SEARCH = "artist.search"
ARTIST_GET = "artist.get"
ARTIST_ALBUMS_GET = "artist.albums.get"
ALBUM_GET = "album.get"

payload = {
    "country" : "US",
    "page" : "1",
    "page_size" : "5",
    "chart_name" : "top",
    "f_has_lyrics" : "1",
    "apikey" : os.getenv("USER_AUTH")
}

def search_artist(artist:str):
    """Returns data of matching artists, formatted by JSON"""
    try:
        artist_search_request = musixmatch_root_URL + ARTIST_SEARCH + f"?q_artist={artist.lower()}&page_size=5&format=json&apikey={os.getenv('USER_Auth')}"
        r = requests.get(artist_search_request)
        data = r.json()
        if data['message']['header']['status_code']!=200:
            sys.exit()
        return data
    except SystemExit:
        print("Try inputting a valid artist!")
    

def reprompt_searched_artist(search_json, index):
    i = index
    if index>=len(search_json['message']['body']['artist_list']):
        print("There are no other artists under this name... quitting program")
        sys.exit()
    print("Is the artist you're looking for: " + search_json['message']['body']['artist_list'][i]['artist']['artist_name'] + "?")
    #Print all artists existing aliases
    if search_json['message']['body']['artist_list'][i]!=None:
        res = "Also known as: "
        for alias in search_json['message']['body']['artist_list'][i]['artist']['artist_alias_list']:
            res += alias['artist_alias'] + ", "
        print(res)
    print("Enter 'no' if this is not the case")
    input = sys.stdin.readline()
    if input.lower()=="no\n":
        return True
    return False

def get_discography(artist_id:int)-> dict:
    """Using the artist_id, get the discography stored by album
    in descending order. Store data into a dictionary with a key 
    of the album id"""
    grab_disc_request = musixmatch_root_URL + ARTIST_ALBUMS_GET + f"?artist_id={artist_id}&s_release_date=desc&g_album_name=1&page_size=100&apikey={os.getenv('USER_Auth')}"
    r = requests.get(grab_disc_request)
    data = r.json()
    #print(data)
    album_list = []
    total_releases = data['message']['body']['album_list']
    #print(total_releases)
    for release in total_releases:
        album = get_album(release['album']['album_id'])
        if album!=[]:
            album_list.append(album)
    return album_list

def get_album(album_id:int)->list:
    """Checks if album is of release type 'album' in which case
    it returns the album_id, album_release_date, and album_name."""
    grab_album_request = musixmatch_root_URL + ALBUM_GET + f"?album_id={album_id}&apikey={os.getenv('USER_Auth')}"
    r = requests.get(grab_album_request)
    data = r.json()
    release = data['message']['body']['album']
    print(data)
    if release['album_release_type']=="Album":
        added_album = []
        added_album.append(release['album_id'])
        added_album.append(release['album_release_date'])
        added_album.append(release['album_name'])
        return added_album
    else:
        return []

    


#new_request = root_URL + CHART_TRACKS_GET + f"?chart_name=top&page=1&page_size=5&country=it&f_has_lyrics=1&apikey={os.getenv('USER_Auth')}"
#print(new_request)
#r = requests.get(new_request)
#data = r.json()
#print(data)
#print(data["message"]["body"]["track_list"][0]["track"]["commontrack_id"])




if __name__=="__main__":
    arguments = sys.argv
    if len(sys.argv)<3:
        raise RuntimeError("There are too little arguments!")
    if len(sys.argv)>5:
        raise RuntimeError("More than four arguments were entered!")
    searching_artist = search_artist(arguments[1])
    #print(selected_artist)
    index = 0
    while True:
        response = reprompt_searched_artist(searching_artist, index)
        index += 1
        if response==False:
            break
    index -= 1
    selected_artist = searching_artist['message']['body']['artist_list'][index]['artist']['artist_id']
    #We have our desired artist at the index
    discography_list = get_discography(selected_artist)
    print(discography_list)


