# Import the necessary modules
import spotipy
import pandas as pd

from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

from dotenv import load_dotenv

import os


class Initializer:
    """
    A class used to initialize the Spotify client and fetch a playlist's tracks.

    ...

    Attributes
    ----------
    playlist_id : str
        The ID of the Spotify playlist to fetch.
    path_to_cache : str
        The path to the cache file where the playlist data will be saved.

    Methods
    -------
    start()
        Fetches the playlist's tracks and saves them to the cache if they are not already there.
    fetch_tracks()
        Fetches all the tracks of the playlist.
    process_tracks(all_tracks)
        Processes the gathered track data.
    is_data_in_cache()
        Checks if the playlist data is already in the cache.
    save_playlist_to_cache(list_of_all_tracks)
        Saves the playlist data to the cache.
    """

    # Constructor 
    def __init__(self, playlist_id, path_to_cache):
        """
        Parameters
        ----------
        playlist_id : str
            The ID of the Spotify playlist to fetch.
        path_to_cache : str
            The path to the cache file where the playlist data will be saved.
        """
        # Load the environment variables from the .env file
        load_dotenv()
        # Retrieve the values of SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET from the environment variables
        os.getenv('SPOTIPY_CLIENT_ID')
        os.getenv('SPOTIPY_CLIENT_SECRET')
        try:   # Initialize the Spotify client with the scope retrieved from the environment variable
            
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=os.getenv('SCOPE')))

            print("Spotify client initialized successfully")

        except Exception as e:   # If an error occurs during initialization, print an error message and set self.sp to None
            
            print("Spotify client initialization failed")
            print(e)

            self.sp = None

        self.playlist_id = playlist_id
        self.path_to_cache = path_to_cache

    def start(self):
        """
        Fetches the playlist's tracks and saves them to the cache if they are not already there.
        """
        # 1. check if the playlist is already in the cache
        # 2. if not, fetch the playlist
        # 2.1 save the playlist to the cache
        # 3. transform the csv into a dataframe
        if self.is_data_in_cache():
            print("Data is in cache")
        else:
            print("Data is not in cache")
            all_tracks = self.fetch_tracks()
            processed_tracks = self.process_tracks(all_tracks)
            self.save_playlist_to_cache(processed_tracks)
            print("Data saved to cache")

    def fetch_tracks(self):
        """
        Fetches all the tracks of the playlist.

        Returns
        -------
        list
            A list of tuples containing the track information.
        """
        all_tracks = [] # initialize an empty list to store the tracks

        # Retrieve the fisrt 100 tracks of the playlist
        print("Gathering tracks...")
        results = self.sp.playlist_tracks(self.playlist_id)
        print(f"Found {results['total']} tracks in the playlist")
    
        # Iterate over the results and append the track information to the all_tracks list
        while results['items']:
            for item in results['items']:
                track       = item['track']
                added_by_id = item['added_by']['id']  # Get the ID of the user who added the track
                
                # Retrieve additional track details
                track_id       = track['id']
                track_name     = track['name']
                track_album    = track['album']['name']
                track_artists  = [artist['name'] for artist in track['artists']]
                track_duration = track['duration_ms']
                
                # append the track to the list of tracks
                all_tracks.append((track_id, track_name, track_album, track_artists, track_duration, added_by_id))
            
            print(f"Gathered {len(all_tracks)} tracks")
        
            # Check if there are more tracks to retrieve (pagination)
            if results['next']:
                results = self.sp.next(results)
            else:
                break

        print("Finished gathering tracks.")

        return all_tracks

    def process_tracks(self, all_tracks):
        """
        Processes the gathered track data.

        Parameters
        ----------
        all_tracks : list
            A list of tuples containing the track information.

        Returns
        -------
        list
            A list of tuples containing the processed track information.
        """
        # Process the gathered data
        processed_tracks = []
        process_iterator = 1
        print("Processing tracks...")
        for (track_id, track_name, track_album, track_artists, track_duration, added_by_id) in all_tracks:
            print(f"Processing track {process_iterator} of {len(all_tracks)}")
            # Make an additional API request to get the user's profile information
            print("started user profile request")
            user          = self.sp.user(added_by_id)
            user_name = user['display_name']  # Get the name of the user who added the track
            user_id       = user['id']  # Get the id of the user who added the track
            print("finished user profile request")
            
            artist_ids = []
            artist_names = []
            genres_set = set()
            for artist_name in track_artists:
                print(f"started artist request for {artist_name}")
                artist_data = self.sp.search(q='artist:' + artist_name, type='artist')
                genres      = artist_data['artists']['items'][0]['genres'] if artist_data['artists']['items'] else []
                artist_id   = artist_data['artists']['items'][0]['id'] if artist_data['artists']['items'] else None  # Get the id of the artist

                artist_ids.append(artist_id)
                artist_names.append(artist_name)
                genres_set.update(genres)
                print(f"finished artist request for {artist_name}")

            genres = list(genres_set)
            
            processed_tracks.append((
                track_id, 
                track_name, 
                track_album, 
                artist_ids,
                artist_names, 
                track_duration, 
                genres, 
                user_id, 
                user_name
            ))
            
            process_iterator += 1
            print(f"Processed {len(processed_tracks)} tracks")

        return processed_tracks




    def is_data_in_cache(self):
        """
        Checks if the playlist data is already in the cache.

        Returns
        -------
        bool
            True if the playlist data is in the cache, False otherwise.
        """
        return os.path.isfile(self.path_to_cache)
    
    def save_playlist_to_cache(self, list_of_all_tracks):
        """
        Saves the playlist data to the cache.

        Parameters
        ----------
        list_of_all_tracks : list
            A list of tuples containing the processed track information.
        """
        # transform the all_tracks list into csv:
        df = pd.DataFrame(list_of_all_tracks, columns=[
        'track_id',
        'track_name',
        'track_album',
        'artist_id',
        'artist_name',
        'track_duration',
        'genres',
        'user_id',
        'user_name'
        ])
        # transform the dataframe into csv
        df.to_csv(self.path_to_cache, index=False)
