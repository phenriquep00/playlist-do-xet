# Import the necessary modules
import spotipy
import pandas as pd

from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

from dotenv import load_dotenv

import os


class Initializer:
    # Constructor 
    def __init__(self, playlist_id, path_to_cache):
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

    def fetch_tracks(self):
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
        # Process the gathered data
        processed_tracks = []
        process_iterator = 1
        print("Processing tracks...")
        for (track_id, track_name, track_album, track_artists, track_duration, added_by_id) in all_tracks:
            print(f"Processing track {process_iterator} of {len(all_tracks)}")
            # Make an additional API request to get the user's profile information
            print("started user profile request")
            user          = self.sp.user(added_by_id)
            added_by_name = user['display_name']  # Get the name of the user who added the track
            print("finished user profile request")
            
            # Make an additional API request to get artist information
            artist_info = []
            for artist_name in track_artists:
                print(f"started artist request for {artist_name}")
                artist_data = self.sp.search(q='artist:' + artist_name, type='artist')
                genres      = artist_data['artists']['items'][0]['genres'] if artist_data['artists']['items'] else []

                artist_info.append({'name': artist_name, 'genres': genres})
                print(f"finished artist request for {artist_name}")

            genres         = [genre for info in artist_info for genre in info['genres']]
            added_by       = added_by_name
            
            # append the processed track to the list of processed tracks
            processed_tracks.append((track_id, track_name, track_album, track_artists, track_duration, genres, added_by))
            process_iterator += 1
            print(f"Processed {len(processed_tracks)} tracks")

        return processed_tracks


    def is_data_in_cache(self):
        return os.path.isfile(self.path_to_cache)
    
    def save_playlist_to_cache(self, list_of_all_tracks):
        # transform the all_tracks list into csv:
        df = pd.DataFrame(list_of_all_tracks, columns=[
        'track_id',
        'track_name',
        'track_album',
        'track_artists',
        'track_duration',
        'genres',
        'added_by',
        ])
        # transform the dataframe into csv
        df.to_csv(self.path_to_cache, index=False)


if __name__ == '__main__':
    initializer = Initializer(
        playlist_id="https://open.spotify.com/playlist/5dhJsu6RdBTBH1XycaO1PA?si=e03ba6ec72394ddf",
        path_to_cache = './data/playlist_data_cache.csv'
    )

    if initializer.sp is not None:
        initializer.start()
    else:
        print("Spotify client initialization failed")
