import os
import time
import requests
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

app = FastAPI()     

CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

# Requirements
# Show a list of the artists you follow.
# Provide an option to stop the currently playing song.
# Provide an option to start playing any of the top 10 songs.
# You can just return a JSON that can be pretty-printed in the browser. UI is NOT needed.
# Deploy the API in your portfolio website itself. Do NOT show the demo on localhost.



# @app.get("/auth/spotify/callback")
# def spotify_callback(code: str):
#     return {"code": code}

# get access token 
def get_access_token():
    res = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    return res.json()['access_token']


@app.get("/spotify/now-playing")
def now_playing():
    token = get_access_token()
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                     headers={"Authorization": f"Bearer {token}"})
    return r.json()

@app.get("/spotify/top-tracks")
def top_tracks():
    token = get_access_token()
    r = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=10",
                     headers={"Authorization": f"Bearer {token}"})
    return r.json()



@app.get("/spotify/followed-artists")
def followed_artists():
    token = get_access_token()
    r = requests.get("https://api.spotify.com/v1/me/following?type=artist",
                     headers={"Authorization": f"Bearer {token}"})
    return r.json()

@app.get("/spotify/play/{track_id}")
def play(track_id: str):
    token = get_access_token()
    r = requests.put("https://api.spotify.com/v1/me/player/play",
                     headers={"Authorization": f"Bearer {token}"},
                     json={"uris": [f"spotify:track:{track_id}"]})
    return {"status": "playing", "track_id": track_id}

@app.get("/spotify/pause")
def pause():
    token = get_access_token()
    r = requests.put("https://api.spotify.com/v1/me/player/pause",
                     headers={"Authorization": f"Bearer {token}"})
    return {"status": "paused"}


 