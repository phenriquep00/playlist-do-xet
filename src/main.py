from lib.spClient import generate_sp_client
from helper.get_last_fetched_track_index import get_last_fetched_track_index
from fetch_tracks import fetch_tracks
from process_tracks import process_tracks
from classes.DatabaseLoader import DatabaseLoader


# TODO: 
# 1. Add documentation to the functions

if __name__ == '__main__':
    sp = generate_sp_client()

    last_fetched_track_index = get_last_fetched_track_index()

    tracks = fetch_tracks(
        sp_client=sp, 
        last_track_index=last_fetched_track_index
        )

    processed_tracks = process_tracks(
        sp_client=sp,
        all_tracks=tracks
    )

    DatabaseLoader().csv_to_db(processed_tracks=processed_tracks)