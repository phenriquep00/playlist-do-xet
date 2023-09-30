import pandas as pd

from helper.setup import setup 
from fetch_tracks import fetch_tracks


def initialize(playlist_id):
    # Set up authentication
    sp = setup()

    # Data caching and fetching
    csv_file = 'playlist_data_cache.csv'

    # check if csv file exists in cache directory and return dataframe if it does exist to avoid calling spotify api
    # if it doesn't exist, call spotify api and create csv file
    try:
        df = pd.read_csv(csv_file)
        print("Data found in cache")
        # TODO: implement the logics to check if new tracks where added to the playlist and update the csv file

        # just return the dataframe without having to call spotify api
        return df
    
    except FileNotFoundError:
        print("Data not found in cache, fetching from Spotify API")
        pass

    # call the api
    all_tracks = fetch_tracks(sp, playlist_id)
    
    # Create a pandas dataframe from the list of tuples
    df = pd.DataFrame(all_tracks, columns=[
        'track_id',
        'track_name',
        'track_album',
        'track_artists',
        'track_duration',
        'genres',
        'added_by',
        ])
    # create csv file
    df.to_csv(csv_file, index=False)
    
    # return dataframe
    return df
