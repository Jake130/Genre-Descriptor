import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


root_URL = "https://api.musixmatch.com/ws/1.1/"
httpbin_base_url = "https://httpbin.org/get" 

CHART_TRACKS_GET = "chart.tracks.get"
CHART_ARTISTS_GET = "chart.artists.get"

payload = {
    "country" : "US",
    "page" : "1",
    "page_size" : "5",
    "chart_name" : "top",
    "f_has_lyrics" : "1",
    "apikey" : os.getenv("USER_AUTH")
}

new_request = root_URL + CHART_TRACKS_GET + f"?chart_name=top&page=1&page_size=5&country=it&f_has_lyrics=1&apikey={os.getenv('USER_Auth')}"
print(new_request)
r = requests.get(new_request)
data = r.json()
print(data["message"]["body"]["track_list"][0]["track"]["commontrack_id"])









query5 = "?firstName=John&lastName=Smith"

parameters = {
    "lastName" : "John",
    "firstName" : "Smith"
}