from classes.Initializer import Initializer
from classes.DatabaseLoader import DatabaseLoader

from utils.csv_to_db import csv_to_db


if __name__ == '__main__':
    PLAYLIST_URI = "https://open.spotify.com/playlist/5dhJsu6RdBTBH1XycaO1PA?si=e03ba6ec72394ddf"


    initializer = Initializer(
        playlist_id=PLAYLIST_URI,
    )

    if initializer.sp is not None:
        processed_tracks = initializer.start()
    else:
        print("Spotify client initialization failed")

    DatabaseLoader().csv_to_db(processed_tracks=processed_tracks)