import matplotlib.pyplot as plt
from initialize import initialize

from analisys.top10_genres import top10_genres
from analisys.top10_artists import top10_artists


PLAYLIST_ID = 'https://open.spotify.com/playlist/5dhJsu6RdBTBH1XycaO1PA?si=e03ba6ec72394ddf'

# PLAYLIST_ID = "https://open.spotify.com/playlist/27aAybWeiTIXFY0uh3X1VW?si=e462516fd54e49e7&pt=28a5de8fb369879be67196b295b3664d"

df = initialize(PLAYLIST_ID)
print(df.head())


top10_artists(df)

