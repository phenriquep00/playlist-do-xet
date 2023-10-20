def process_tracks(sp_client, all_tracks):
        # Process the gathered data
        processed_tracks = []
        process_iterator = 1
        print("Processing tracks...")
        for (track_id, track_name, track_album, track_artists, track_duration, added_by_id) in all_tracks:
            print(f"Processing track {process_iterator} of {len(all_tracks)}")
            # Make an additional API request to get the user's profile information
            # TODO: check if the user already exists on db, if so just get the info from it, and if not do the api request
            user          = sp_client.user(added_by_id)
            user_name     = user['display_name']  # Get the name of the user who added the track
            user_id       = user['id']  # Get the id of the user who added the track
            
            artist_ids   = []
            artist_names = []
            genres_set   = set()
            for artist_name in track_artists:
                artist_data = sp_client.search(q='artist:' + artist_name, type='artist')
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
            print(f"Processed {process_iterator - 1}° track with results -> NAME: {track_name} | ARTISTS: {track_artists} | ADDED_BY: {user_name}")

        return processed_tracks