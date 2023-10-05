from dotenv import load_dotenv

import os

load_dotenv()


def fetch_tracks(sp_client, last_track_index=None):
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
            results = sp_client.playlist_tracks(
                os.environ["PLAYLIST_URI"], offset=offset, limit=100
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