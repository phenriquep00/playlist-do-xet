from classes.Initializer import Initializer
from utils.csv_to_db import csv_to_db


if __name__ == '__main__':
    PLAYLIST_URI = "https://open.spotify.com/playlist/5dhJsu6RdBTBH1XycaO1PA?si=e03ba6ec72394ddf"
    PATH_TO_CACHE = './data/playlist_data_cache.csv'


    initializer = Initializer(
        playlist_id=PLAYLIST_URI,
        path_to_cache = PATH_TO_CACHE
    )

    if initializer.sp is not None:
        initializer.start()
    else:
        print("Spotify client initialization failed")

    csv_to_db(PATH_TO_CACHE)