from spotipy.exceptions import SpotifyException

def fetch_tracks(sp, playlist_id):
    # Initialize an empty list to store all tracks
    all_tracks = []

    # Initial request to get the first 100 tracks
    print("Gathering tracks...")
    results = sp.playlist_tracks(playlist_id, market='US')
    print(f"Found {results['total']} tracks in the playlist")

    # Loop through the tracks and retrieve track details
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
            results = sp.next(results)
        else:
            break

    print("Finished gathering tracks.")

    # Process the gathered data
    processed_tracks = []
    process_iterator = 1
    print("Processing tracks...")
    for (track_id, track_name, track_album, track_artists, track_duration, added_by_id) in all_tracks:
        print(f"Processing track {process_iterator} of {len(all_tracks)}")
        # Make an additional API request to get the user's profile information
        print("started user profile request")
        user          = sp.user(added_by_id)
        added_by_name = user['display_name']  # Get the name of the user who added the track
        print("finished user profile request")
        
        # Make an additional API request to get artist information
        artist_info = []
        for artist_name in track_artists:
            print(f"started artist request for {artist_name}")
            artist_data = sp.search(q='artist:' + artist_name, type='artist')
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
