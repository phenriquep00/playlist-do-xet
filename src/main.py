from classes.Initializer import Initializer


if __name__ == '__main__':
    initializer = Initializer(
        playlist_id="https://open.spotify.com/playlist/5dhJsu6RdBTBH1XycaO1PA?si=e03ba6ec72394ddf",
        path_to_cache = './data/playlist_data_cache.csv'
    )

    if initializer.sp is not None:
        initializer.start()
    else:
        print("Spotify client initialization failed")
