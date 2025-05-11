# import os
# import time
# import requests
# from fastapi import FastAPI, HTTPException, Path
# from pydantic import BaseModel

# app = FastAPI()     




# # get authorization code manually once
# # spotify will send the code on this endpoint
# # @app.get("/auth/spotify/callback")
# # def spotify_callback(code: str):
# #     return {"code": code}



# from base64 import b64encode

# def get_access_token():
#     client_id     = os.getenv("CLIENT_ID")
#     client_secret = os.getenv("CLIENT_SECRET")
#     refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
#     if not all([client_id, client_secret, refresh_token]):
#         raise HTTPException(500, "Missing one of CLIENT_ID/CLIENT_SECRET/SPOTIFY_REFRESH_TOKEN")

#     auth_header = b64encode(f"{client_id}:{client_secret}".encode()).decode()
#     resp = requests.post(
#         "https://accounts.spotify.com/api/token",
#         data={
#             "grant_type":    "refresh_token",
#             "refresh_token": refresh_token
#         },
#         headers={
#             "Authorization": f"Basic {auth_header}",
#             "Content-Type":  "application/x-www-form-urlencoded"
#         }
#     )
#     data = resp.json()
#     if resp.status_code != 200 or "access_token" not in data:
#         # Returns HTTP 502 with Spotify's error JSON
#         raise HTTPException(502, f"Token refresh failed: {data}")
#     return data["access_token"]


# @app.get("/spotify/now-playing")
# def now_playing():
#     token = get_access_token()
#     r = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
#                      headers={"Authorization": f"Bearer {token}"})
#     return r.json()

# @app.get("/spotify/top-tracks")
# def top_tracks():
#     token = get_access_token()
#     r = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=10",
#                      headers={"Authorization": f"Bearer {token}"})
#     return r.json()



# @app.get("/spotify/followed-artists")
# def followed_artists():
#     token = get_access_token()
#     r = requests.get("https://api.spotify.com/v1/me/following?type=artist",
#                      headers={"Authorization": f"Bearer {token}"})
#     return r.json()

# @app.put("/spotify/play/{track_id}")
# def play_track(track_id: str):
#     token = get_access_token()
#     body={"uris": [f"spotify:track:{track_id}"]}
#     r = requests.put("https://api.spotify.com/v1/me/player/play",
#                      headers={"Authorization": f"Bearer {token}","Content-Type": "application/json"},
#                      json=body)
#     print(r)
#     return {"status": r.status_code, "track_id": track_id}



# @app.put("/spotify/pause")
# def pause_playback():
#     token = get_access_token()
#     r = requests.put(
#         "https://api.spotify.com/v1/me/player/pause",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     print(r)
#     return {"status": r.status_code}


 







 