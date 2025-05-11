import os
import time
import requests
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

app = FastAPI()  

CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
REDIRECT_URI  = os.getenv("SPOTIFY_REDIRECT_URI")

@app.get("/auth/spotify/callback")
def spotify_callback(code: str):
    return {"code": code}

 