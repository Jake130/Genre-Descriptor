import requests
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
ALBUM_TRACKS_GET = "album.tracks.get"
MATCHER_TRACK_GET = "matcher.track.get"
TRACK_LYRICS_MOOD_GET = "track.lyrics.mood.get"

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
        print("There was an issue searching the artist in MusixMatch")
        return None
    
def get_artist_albums(artist_id, p_num):
    get_albums_request = musixmatch_root_URL + ARTIST_ALBUMS_GET + f"?artist_id={artist_id}&s_release_date=desc&g_album_name=1&page={p_num}&page_size=5&apikey={os.getenv('USER_Auth')}"
    r = requests.get(get_albums_request)
    data = r.json()
    return data

def check_albums_matching(release_list, latest:str) -> bool:
    """Sees if the artist's latest release is in the list of releases."""
    for release in release_list['message']['body']['album_list']:
        if release['album']['album_name'].lower()==latest.lower():
            return True
    return False

def reprompt_searched_artist(search_json, index):
    if index>=len(search_json['message']['body']['artist_list']):
        print("There are no other artists under this name... quitting program")
        sys.exit()
    print("Is the artist you're looking for: " + search_json['message']['body']['artist_list'][index]['artist']['artist_name'] + "?")
    #Print all artists existing aliases
    if search_json['message']['body']['artist_list'][index]!=None:
        res = "Also known as: "
        for alias in search_json['message']['body']['artist_list'][index]['artist']['artist_alias_list']:
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


def match_albums(albums_data, artist):
    """Matches the albums taken from spotify with
    the ones in musixmatch (ten most popular). Exits
    program if no match can be found. Returns up to 
    their 10 most popular albums"""
    searched_artist = search_artist(artist)
    index = 0
    latest = albums_data[0][1]
    albums = get_artist_albums(searched_artist['message']['body']['artist_list'][index]['artist']['artist_id'], 1)
    #We are using the artists exact name, only getting 5 artists is fine...
    while (albums['message']['header']['status_code']==200):
        if check_albums_matching(albums, latest)==True:
            break
        else:
            index += 1
            #print(index)
            if index >5:
                break
            albums = get_artist_albums(searched_artist['message']['body']['artist_list'][index]['artist']['artist_id'], 1)
    if (albums['message']['header']['status_code']!=200 or index>5):
        print("It doesn't seem like this artist is in Musixmatch, could find no matches with Spotify Data...")
        sys.exit()
    #We've matched the artist (specified by index) and have their first couple of releases
    #Get rest of the albums, dicard ones that are not neeeded
    #Call our stored albums STORED_ALBUMS
    lower_albums = [i[1].lower() for i in albums_data]
    album_ids_popularity = []
    count = 0
    offset = 0
    page_number = 1
    while count<len(albums_data):
        for release in albums['message']['body']['album_list']:
            offset += 1
            if release['album']['album_name'].lower() in lower_albums:
                count += 1
                album_ids_popularity.append((release['album']['album_id'], release['album']['album_name'], release['album']['album_rating']))
        #Special break case for last block of releases
        if count==len(albums_data):
            break
        page_number += 1
        #Get next page unless there is none
        albums = get_artist_albums(searched_artist['message']['body']['artist_list'][index]['artist']['artist_id'], page_number)
        if albums['message']['body']['album_list']==[]:
            break
    album_ids_popularity.sort(key=lambda tup: tup[2], reverse=True)
    return album_ids_popularity[0:10]

def map_album_total(top_albums, albums_data)->dict[str:int]:
    """Creates dictionary mapping of album name to total tracks
    on that album"""
    m_album_total = {}
    for album in albums_data:
        for top in top_albums:
            if album[1].lower()==top[1].lower():
                m_album_total[top[1]] = album[2]
                break
    return m_album_total

def get_top_album_tracks(top_albums, m_album_total):
    #404 if it didn't work
    #Get tuples of all commontrack_ids for each album
    total_tracks = []
    for top in top_albums:
        get_tracks_from_albums = musixmatch_root_URL + ALBUM_TRACKS_GET + f"?album_id={top[0]}&page_size={m_album_total[top[1]]}&apikey={os.getenv('USER_Auth')}"
        r = requests.get(get_tracks_from_albums)
        data = r.json()
        total_tracks.append(tuple(track['track']['commontrack_id'] for track in data['message']['body']['track_list']))
        print("here")
    return total_tracks

def get_moods(commontrack_id):
    get_moods_request = musixmatch_root_URL + TRACK_LYRICS_MOOD_GET + f"?commontrack_id={commontrack_id}&apikey={os.getenv('USER_Auth')}"
    r = requests.get(get_moods_request)
    data = r.json()
    print(data)

def get_all_moods(all_tracks:list[tuple[int]])->list[list[list]]:
    all_moods = []
    for album in all_tracks:
        album_moods = []
        for commontrack_id in album:
            album_moods.append(get_moods(commontrack_id)['message']['body']['mood_list'])
        all_moods.append(album_moods)
    return all_moods


if __name__=="__main__":
    top_albums = match_albums([('6ofEQubaL265rIW6WnCU8y', 'KID A MNESIA', 34, '2021-11-05', 'album', 'https://i.scdn.co/image/ab67616d00001e02bbaaa8bf9aedb07135d2c6d3'), ('0tzfI6NFJqcJkWb23R3lRZ', 'OK Computer OKNOTOK 1997 2017', 23, '2017-06-23', 'album', 'https://i.scdn.co/image/ab67616d00001e02ee58b8ce747da91d69a862cc'), ('2ix8vWvvSp2Yo7rKMiWpkg', 'A Moon Shaped Pool', 11, '2016-05-08', 'album', 'https://i.scdn.co/image/ab67616d00001e0245643f5cf119cbc9d2811c22'), ('566osTxDsfrtdBxPDMGufx', 'TKOL RMX 1234567', 19, '2011-10-10', 'album', 'https://i.scdn.co/image/ab67616d00001e02c5d47a9a4553e4cca882162c'), ('3P17levwUPzmFfLYdAK3A7', 'The King Of Limbs', 8, '2011-02-18', 'album', 'https://i.scdn.co/image/ab67616d00001e02a9be6a9b8b5831a4c431ab9f'), ('5vkqYmiPBYLaalcmjujWxK', 'In Rainbows', 10, '2007-12-28', 'album', 'https://i.scdn.co/image/ab67616d00001e02de3c04b5fc750b68899b20a9'), ('6zTAW5oRuOmxJuUHhcQope', 'In Rainbows (Disk 2)', 8, '2007', 'album', 'https://i.scdn.co/image/ab67616d00001e024b88d5c1b3358cca2c94ec0b'), ('5mzoI3VH0ZWk1pLFR6RoYy', 'Hail To the Thief', 14, '2003-06-09', 'album', 'https://i.scdn.co/image/ab67616d00001e020da53e8f58e59f28a79c10c7'), ('1vdQ5t7iO2gC3OX7j2GFCt', 'I Might Be Wrong', 8, '2001-11-12', 'album', 'https://i.scdn.co/image/ab67616d00001e0205a2f9af5f0eaed4835acf54'), ('1HrMmB5useeZ0F5lHrMvl0', 'Amnesiac', 11, '2001-03-12', 'album', 'https://i.scdn.co/image/ab67616d00001e02863e0e305637100311c91aa7'), ('6GjwtEZcfenmOf6l18N7T7', 'Kid A', 11, '2000-10-02', 'album', 'https://i.scdn.co/image/ab67616d00001e026c7112082b63beefffe40151'), ('6dVIqQ8qmQ5GBnJ9shOYGE', 'OK Computer', 12, '1997-05-28', 'album', 'https://i.scdn.co/image/ab67616d00001e02c8b444df094279e70d0ed856'), ('35UJLpClj5EDrhpNIi4DFg', 'The Bends', 12, '1995-03-13', 'album', 'https://i.scdn.co/image/ab67616d00001e029293c743fa542094336c5e12'), ('3gBVdu4a1MMJVMy6vwPEb8', 'Pablo Honey', 12, '1993-02-22', 'album', 'https://i.scdn.co/image/ab67616d00001e02df55e326ed144ab4f5cecf95')], "radiohead")
    m_dict = map_album_total(top_albums, [('6ofEQubaL265rIW6WnCU8y', 'KID A MNESIA', 34, '2021-11-05', 'album', 'https://i.scdn.co/image/ab67616d00001e02bbaaa8bf9aedb07135d2c6d3'), ('0tzfI6NFJqcJkWb23R3lRZ', 'OK Computer OKNOTOK 1997 2017', 23, '2017-06-23', 'album', 'https://i.scdn.co/image/ab67616d00001e02ee58b8ce747da91d69a862cc'), ('2ix8vWvvSp2Yo7rKMiWpkg', 'A Moon Shaped Pool', 11, '2016-05-08', 'album', 'https://i.scdn.co/image/ab67616d00001e0245643f5cf119cbc9d2811c22'), ('566osTxDsfrtdBxPDMGufx', 'TKOL RMX 1234567', 19, '2011-10-10', 'album', 'https://i.scdn.co/image/ab67616d00001e02c5d47a9a4553e4cca882162c'), ('3P17levwUPzmFfLYdAK3A7', 'The King Of Limbs', 8, '2011-02-18', 'album', 'https://i.scdn.co/image/ab67616d00001e02a9be6a9b8b5831a4c431ab9f'), ('5vkqYmiPBYLaalcmjujWxK', 'In Rainbows', 10, '2007-12-28', 'album', 'https://i.scdn.co/image/ab67616d00001e02de3c04b5fc750b68899b20a9'), ('6zTAW5oRuOmxJuUHhcQope', 'In Rainbows (Disk 2)', 8, '2007', 'album', 'https://i.scdn.co/image/ab67616d00001e024b88d5c1b3358cca2c94ec0b'), ('5mzoI3VH0ZWk1pLFR6RoYy', 'Hail To the Thief', 14, '2003-06-09', 'album', 'https://i.scdn.co/image/ab67616d00001e020da53e8f58e59f28a79c10c7'), ('1vdQ5t7iO2gC3OX7j2GFCt', 'I Might Be Wrong', 8, '2001-11-12', 'album', 'https://i.scdn.co/image/ab67616d00001e0205a2f9af5f0eaed4835acf54'), ('1HrMmB5useeZ0F5lHrMvl0', 'Amnesiac', 11, '2001-03-12', 'album', 'https://i.scdn.co/image/ab67616d00001e02863e0e305637100311c91aa7'), ('6GjwtEZcfenmOf6l18N7T7', 'Kid A', 11, '2000-10-02', 'album', 'https://i.scdn.co/image/ab67616d00001e026c7112082b63beefffe40151'), ('6dVIqQ8qmQ5GBnJ9shOYGE', 'OK Computer', 12, '1997-05-28', 'album', 'https://i.scdn.co/image/ab67616d00001e02c8b444df094279e70d0ed856'), ('35UJLpClj5EDrhpNIi4DFg', 'The Bends', 12, '1995-03-13', 'album', 'https://i.scdn.co/image/ab67616d00001e029293c743fa542094336c5e12'), ('3gBVdu4a1MMJVMy6vwPEb8', 'Pablo Honey', 12, '1993-02-22', 'album', 'https://i.scdn.co/image/ab67616d00001e02df55e326ed144ab4f5cecf95')])
    print(top_albums)
    print(m_dict)
    total_tracks = get_top_album_tracks(top_albums, m_dict) #Output sorted by popularity, only need commontrack_id
    print(total_tracks)
    get_moods(13484)
    """Implementation would be...
    -getting moods for every song stored as list[tup[tup[str]]]
    -processing a ranking for every song stored as list[tup[int]]
    -for album_rankings in total-rankings"""