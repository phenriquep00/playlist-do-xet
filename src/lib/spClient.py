import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

import os


def generate_sp_client():


    try:   # Initialize the Spotify client with the scope retrieved from the environment variable

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=os.getenv('SCOPE')))

        print("Spotify client initialized successfully")

    except Exception as e:   # If an error occurs during initialization, print an error message and set self.sp to None

        print("Spotify client initialization failed")
        print(e)

        sp = None

    return sp