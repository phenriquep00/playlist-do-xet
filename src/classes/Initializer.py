# Import the necessary modules
import spotipy
import pandas as pd
import mysql.connector

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

        all_tracks = self.fetch_tracks(
            last_track_index=self.get_last_fetched_track_index()
        )
        processed_tracks = self.process_tracks(all_tracks)
        self.save_playlist_to_cache(processed_tracks)
        print("Data saved to cache")

    def fetch_tracks(self, last_track_index=None):
        """
        Fetches all the tracks of the playlist starting from the last_track_index if provided.

        Parameters
        ----------
        last_track_index : int, optional
            The index of the last track from which to start fetching. If None, fetch all tracks.

        Returns
        -------
        list
            A list of tuples containing the track information.
        """
        all_tracks = []  # Initialize an empty list to store the tracks

        # Initialize the offset for pagination
        offset = 0

        # Continue fetching until there are no more tracks to retrieve
        while True:
            # Fetch the next batch of tracks from the playlist with the specified offset
            print(f"Gathering tracks with offset {offset}...")
            results = self.sp.playlist_tracks(
                self.playlist_id, offset=offset, limit=100
            )

            # If there are no items in the results, break the loop
            if not results['items']:
                break

            for index, item in enumerate(results['items'], start=offset):
                track = item['track']
                added_by_id = item['added_by']['id']  # Get the ID of the user who added the track

                # Retrieve additional track details
                track_id = track['id']
                track_name = track['name']
                track_album = track['album']['name']
                track_artists = [artist['name'] for artist in track['artists']]
                track_duration = track['duration_ms']

                # Append the track to the list of tracks if it's newer than the last_track_index
                if last_track_index is None or index > last_track_index:
                    all_tracks.append((track_id, track_name, track_album, track_artists, track_duration, added_by_id))

            print(f"Gathered {len(all_tracks)} tracks")

            # Check if there are more tracks to retrieve (pagination)
            if results['next']:
                offset += 100  # Increment the offset for the next batch
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

    
    def save_playlist_to_cache(self, list_of_new_tracks):
        """
        Appends the new track data to the cache file.

        Parameters
        ----------
        list_of_new_tracks : list
            A list of tuples containing the processed track information for new tracks.
        """
        # Check if the cache file already exists
        if os.path.isfile(self.path_to_cache):
            # If it exists, open it in append mode
            with open(self.path_to_cache, 'a', newline='', encoding='utf-8') as f:
                # Create a DataFrame for the new tracks
                df = pd.DataFrame(list_of_new_tracks, columns=[
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
                # Append the new data to the end of the file
                df.to_csv(f, mode='a', header=False, index=False)
        else:
            # If it doesn't exist, create a new file
            df = pd.DataFrame(list_of_new_tracks, columns=[
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
            df.to_csv(self.path_to_cache, index=False)

    def get_last_fetched_track_index(self):
        """
        Retrieves the index of the last fetched track from the database.

        Returns
        -------
        int or None
            The index of the last fetched track or None if no tracks have been fetched yet.
        """
        try:
            # Establish a connection to the database
            mydb = mysql.connector.connect(
                host=os.getenv("DB_CONNECTION_HOST"),
                user=os.getenv("DB_CONNECTION_USER"),
                password=os.getenv("DB_CONNECTION_PASSWORD"),
                database=os.getenv("DB_CONNECTION_DATABASE")
            )

            mycursor = mydb.cursor()

            # Execute a query to count the number of rows in the Tracks table
            query = "SELECT COUNT(*) FROM Tracks"
            mycursor.execute(query)

            last_track_index = mycursor.fetchone()[0]

            # Close the database connection
            mydb.close()

            return last_track_index

        except Exception as e:
            print(f"Error fetching last track index from the database: {e}")
            return None
