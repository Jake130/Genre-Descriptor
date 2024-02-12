from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

REDIRECT_URI="http://localhost:3000"
API_BASE_URL="https://api.spotify.com/v1/"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

parameters = {
    "grant_type" : "client_credentials",
    "client_id" : os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret" : os.getenv("SPOTIFY_CLIENT_SECRET")
}

def get_access():
    r = requests.post(TOKEN_URL, headers={"Content-Type" : "application/x-www-form-urlencoded"}, params=parameters)
    data = r.json()
    return data



if __name__=="__main__":
    token_json = get_access()
    print(token_json)