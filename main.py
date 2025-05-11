# updated later,old one id main_old 

import os
import requests
from fastapi import FastAPI, HTTPException,status
from base64 import b64encode


app = FastAPI()     

SPOTIFY_API_BASE="https://api.spotify.com/v1"


# Requirements
# Show a list of the artists you follow.
# Provide an option to stop the currently playing song.
# Provide an option to start playing any of the top 10 songs.
# You can just return a JSON that can be pretty-printed in the browser. UI is NOT needed.
# Deploy the API in your portfolio website itself. Do NOT show the demo on localhost.

# Steps----->
# 1. Go to sptify developer dashboard and get the client secret and id . Paste a dummy link in redirect_uri.
# 2. Deploy it with secret and it .
# 3. Get the deployed link
# 4. Update in redirect_uri in spotify developer dashboard and also in .env file 
# 5. Send a request to spotify asking for permisssion with client_id,client_secret,redirect_uri,scopes 
# https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=YOUR_REDIRECT_URI&scope=user-read-playback-state user-read-currently-playing user-top-read user-follow-read user-modify-playback-state

# 6. Spotify will send a code get it via making a get request to auth/spotify/callback
# 7. Make a post request with that temporary code to get refresh token
 
# get authorization code manually once
# spotify will send the code on this uri -- REDIRECT_URI
# code will be received after confirmation by spotify that api can interact with spotify 

# @app.get("/auth/spotify/callback")
# def spotify_callback(code: str):
#     return {"code": code}

# post request to get the tokens

# curl -X POST https://accounts.spotify.com/api/token \
# -H "Content-Type: application/x-www-form-urlencoded" \
# -d "grant_type=authorization_code" \
# -d "code=PASTE CODE RECEIVED AFTER SPOTIFY APPROVAL" \
# -d "redirect_uri=PASTE REDIRECT_URI" \
# -d "client_id=PASTE CLIENT _ID" \
# -d "client_secret=PASTE CLIENT_SECRET"

 

# get access token from SPOTIFY_REFRESH_TOKEN
def get_access_token():
    client_id     = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
    if not all([client_id, client_secret, refresh_token]):
        raise HTTPException(500, "Missing one of SPOTIFY_CLIENT_ID/SECRET/REFRESH_TOKEN")

    auth_header = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type":    "refresh_token",
            "refresh_token": refresh_token
        },
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type":  "application/x-www-form-urlencoded"
        }
    )
    data = resp.json()
    if resp.status_code != 200 or "access_token" not in data:
        # Returns HTTP 502 with Spotify's error JSON
        raise HTTPException(502, f"Token refresh failed: {data}")
    return data["access_token"]


def spotify_request(method: str, endpoint: str, **kwargs):
    url = f"{SPOTIFY_API_BASE}/{endpoint}"
    token=get_access_token()

    headers=kwargs.pop("headers",{})
    headers["Authorization"]=f"Bearer{token}"
    
    try:
        resp = requests.request(method, url, headers=headers,**kwargs)
    except requests.RequestException as e:
        # network or DNS error, timeout, etc.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Network error talking to Spotify: {e}"
        )
    
    if resp.status_code == 204:
        return None

    # Now the HTTP request succeeded—inspect resp.status_code
    if 200 <= resp.status_code < 300: 
        return resp.json()

    # Spotify returned an error status.  Forward it:
    raise HTTPException(
        status_code=resp.status_code,        
        detail=f"Spotify API error {resp.status_code}: {resp.text}"
    )



@app.get("/spotify/now-playing")
def now_playing():
    SPOTIFY_ENDPOINT="me/player/currently-playing"
    r=spotify_request("GET",SPOTIFY_ENDPOINT)
    
    return r

@app.get("/spotify/top-tracks")
def top_tracks():
    SPOTIFY_ENDPOINT="me/top/tracks?limit=10"
    r=spotify_request("GET",SPOTIFY_ENDPOINT)

    return r



@app.get("/spotify/followed-artists")
def followed_artists():
    SPOTIFY_ENDPOINT="me/following?type=artist"
    r=spotify_request("GET",SPOTIFY_ENDPOINT)

    return r

@app.put("/spotify/play/{track_id}")
def play_track(track_id: str):
    body={"uris": [f"spotify:track:{track_id}"]}
    SPOTIFY_ENDPOINT="me/player/play"
    r=spotify_request("PUT",SPOTIFY_ENDPOINT,json=body)

   
    print(r)
    return {"status": r.status_code, "is_playing": r.is_playing}


@app.put("/spotify/pause")
def pause_playback():
    SPOTIFY_ENDPOINT="me/player/pause"
    r=spotify_request("PUT",SPOTIFY_ENDPOINT)
    print(r)
    return {"status": r.status_code}