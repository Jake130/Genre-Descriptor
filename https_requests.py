import requests
import json
from dotenv import load_dotenv
import os
import sys

load_dotenv()

root_URL = "https://api.musixmatch.com/ws/1.1/"
httpbin_base_url = "https://httpbin.org/get" 

CHART_TRACKS_GET = "chart.tracks.get"
CHART_ARTISTS_GET = "chart.artists.get"
ARTIST_SEARCH = "artist.search"
ARTIST_GET = "artist.get"
ARTIST_ALBUMS_GET = "artist.albums.get"

payload = {
    "country" : "US",
    "page" : "1",
    "page_size" : "5",
    "chart_name" : "top",
    "f_has_lyrics" : "1",
    "apikey" : os.getenv("USER_AUTH")
}

def search_artist(artist:str):
    try:
        artist_search_request = root_URL + ARTIST_SEARCH + f"?q_artist={artist.lower()}&page_size=5&format=json&apikey={os.getenv('USER_Auth')}"
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
    res = "Also known as: "
    for alias in search_json['message']['body']['artist_list'][i]['artist']['artist_alias_list']:
        res += alias['artist_alias'] + ", "
    print(res)
    print("Enter 'no' if this is not the case")
    input = sys.stdin.readline()
    if input.lower()=="no\n":
        return True
    return False
    


#new_request = root_URL + CHART_TRACKS_GET + f"?chart_name=top&page=1&page_size=5&country=it&f_has_lyrics=1&apikey={os.getenv('USER_Auth')}"
#print(new_request)
#r = requests.get(new_request)
#data = r.json()
#print(data)
#print(data["message"]["body"]["track_list"][0]["track"]["commontrack_id"])




if __name__=="__main__":
    arguments = sys.argv
    print(len(sys.argv))
    if len(sys.argv)<3:
        raise RuntimeError("There are too little arguments!")
    if len(sys.argv)>5:
        raise RuntimeError("More than four arguments were entered!")
    selected_artist = search_artist(arguments[1])
    #print(selected_artist)
    index = 0
    while True:
        response = reprompt_searched_artist(selected_artist, index)
        index += 1
        if response==False:
            break
    print(response)
        
    print("Exited the loop")

