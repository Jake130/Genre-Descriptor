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
    query = API_BASE_URL + "artists" + f"/{artist_id}" + f"/albums" + f"?include_groups={release_type}&market=US&limit=50"
    r = requests.get(query, headers=authorization_dict)
    data = r.json()
    release_list = []
    #Fmax = 0
    #data['items'].sort(key=lambda rel: rel['popularity'])
    for release in data['items']:
        #track_names = get_track_names(release['id'])
        release_list.append((release['id'], release['name'], release['total_tracks'], release['release_date'], release['album_group'], release['images'][1]['url']))
        #max += 1
        #if max>=10:
        #    break
    return release_list

def get_album_data(release_list):
    length = len(release_list)
    album_ids = []
    j = 0
    k = 20
    while (length-20)>0:    #Handles chunks of 20 (limit for next API call)
        new_ids = ""
        for i in range(j,k):
            if i < k-1:
                new_ids += f"{release_list[i][0]},"
            else:
                new_ids += f"{release_list[i][0]}"
        album_ids.append(new_ids)
        j += 20
        k += 20
        length -= 20
    new_ids = ""
    for i in range(j, len(release_list)):       #Handles the remaining number
        if i < len(release_list)-1:
            new_ids += f"{release_list[i][0]},"
        else:
            new_ids += f"{release_list[i][0]}"
    album_ids.append(new_ids)
    total = []
    for i in range(0, len(album_ids)):
        query = API_BASE_URL + f"albums" + f"?ids={album_ids[i]}"
        r = requests.get(query, headers=authorization_dict)
        data = r.json()
        total += data["albums"]
    return data['albums']

def make_top_ten(albums_data):
    albums_data.sort(key=lambda json: json["popularity"], reverse=True)
    return albums_data[0:10]

def get_tracks_popularity(top_ten):
    """From the data gathered on top 10 tracks, make a list of tuples representing
    each album, containing integers representing each track's popularity."""
    #length = len(top_ten)
    complete_ratings = []
    track_ids = []
    new_ids = ""
    for i in range(0, len(top_ten)):       #Handles the remaining number
        #print(f"Total Tracks: {top_ten[i]['total_tracks']}, Track Name: {top_ten[i]['name']}")
        new_ids = ""
        for m in range(top_ten[i]['total_tracks']):
            new_ids += f"{top_ten[i]['tracks']['items'][m]['id']},"
        track_ids.append(new_ids[:-1])

    #add to complete ratings
    for i in range(0, len(track_ids)):
        query = API_BASE_URL + f"tracks" + f"?ids={track_ids[i]}"
        r = requests.get(query, headers=authorization_dict)
        data = r.json()
        #print(data)
        for i in data['tracks']:
            complete_ratings.append(i["popularity"])
    return complete_ratings

def get_track_names(album_id):
    query = API_BASE_URL + "albums" + f"/{album_id}"
    r = requests.get(query, headers=authorization_dict)
    data = r.json()
    track_names = []
    for track in data['tracks']['items']:
        track_names.append(track['name'])
    return track_names

def partition_rankings(top_ten, complete_ratings):
    """Group total track rankings by album."""
    partitioned_ratings = []
    index = 0
    for album in top_ten:
        total_tracks = album['total_tracks']
        grouping = []
        for track in range(total_tracks):
            grouping.append(complete_ratings[index])
            index += 1
        partitioned_ratings.append(tuple(grouping))
    return partitioned_ratings

if __name__=="__main__":
    print("Running \"spotify_requests.py\" is reserved for testing.")
    releases = get_discography("4q3ewBCX7sLwd24euuV69X")
    albums_data = get_album_data(releases)
    top_ten = make_top_ten(albums_data)
    for top in top_ten:
        print(top["popularity"])
    #print(top_ten)
    #print(top_ten[0]["tracks"])
    complete_ratings = get_tracks_popularity(top_ten)
    print(len(complete_ratings))
    partitioned_ratings = partition_rankings(top_ten, complete_ratings)
    print(complete_ratings)
    print(partitioned_ratings)

