import csv
import mysql.connector
import ast
from dotenv import load_dotenv
import os


def csv_to_db(csv_file):

    load_dotenv()

    # Establish a MySQL connection
    mydb = mysql.connector.connect(
        host=os.getenv("DB_CONNECTION_HOST"),
        user=os.getenv("DB_CONNECTION_USER")),
        password=os.getenv("DB_CONNECTION_PASSWORD"),
        database=os.getenv("DB_CONNECTION_DATABASE")
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Open the CSV file with utf-8 encoding
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check if user exists before inserting into Users table
            sql = "SELECT * FROM Users WHERE user_id = %s"
            val = (row['user_id'],)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            if not result:
                sql = "INSERT INTO Users (user_id, user_name) VALUES (%s, %s)"
                val = (row['user_id'], row['user_name'])
                mycursor.execute(sql, val)

            # Check if track exists before inserting into Tracks table
            sql = "SELECT * FROM Tracks WHERE track_id = %s"
            val = (row['track_id'],)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            if not result:
                sql = "INSERT INTO Tracks (track_id, track_name, track_album, track_duration, added_by) VALUES (%s, %s, %s, %s, %s)"
                val = (row['track_id'], row['track_name'], row['track_album'], row['track_duration'], row['user_id'])
                mycursor.execute(sql, val)

            # Insert data into Artists table and TrackArtists table
            artist_ids = ast.literal_eval(row['artist_id'])
            artist_names = ast.literal_eval(row['artist_name'])
            for artist_id, artist_name in zip(artist_ids, artist_names):
                # If artist_id is null, insert "No Artist"
                if artist_id is None:
                    artist_id = "No Artist"

                # Check if artist exists before inserting into Artists table
                sql = "SELECT * FROM Artists WHERE artist_id = %s"
                val = (artist_id,)
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                if not result:
                    sql = "INSERT INTO Artists (artist_id, artist_name) VALUES (%s, %s)"
                    val = (artist_id, artist_name)
                    mycursor.execute(sql, val)

                # Check if track-artist relation exists before inserting into TrackArtists table
                sql = "SELECT * FROM TrackArtists WHERE track_id = %s AND artist_id = %s"
                val = (row['track_id'], artist_id)
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                if not result:
                    sql = "INSERT INTO TrackArtists (track_id, artist_id) VALUES (%s, %s)"
                    val = (row['track_id'], artist_id)
                    mycursor.execute(sql, val)

            # Insert data into Genres table and TrackGenres table
            genres = ast.literal_eval(row['genres'])
            for genre in genres:
                # Check if genre exists before inserting into Genres table
                sql = "SELECT genre_id FROM Genres WHERE genre_name = %s"
                val = (genre,)
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                if not result:
                    sql = "INSERT INTO Genres (genre_name) VALUES (%s)"
                    val = (genre,)
                    mycursor.execute(sql, val)
                    mycursor.execute("SELECT LAST_INSERT_ID()")
                    genre_id = mycursor.fetchone()[0]
                else:
                    genre_id = result[0][0]

                # Check if track-genre relation exists before inserting into TrackGenres table
                sql = "SELECT * FROM TrackGenres WHERE track_id = %s AND genre_id = %s"
                val = (row['track_id'], genre_id)
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                if not result:
                    sql = "INSERT INTO TrackGenres (track_id, genre_id) VALUES (%s, %s)"
                    val = (row['track_id'], genre_id)
                    mycursor.execute(sql, val)

            # Insert data into UserTracks table
            sql = "SELECT * FROM UserTracks WHERE user_id = %s AND track_id = %s"
            val = (row['user_id'], row['track_id'])
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            if not result:
                sql = "INSERT INTO UserTracks (user_id, track_id) VALUES (%s, %s)"
                val = (row['user_id'], row['track_id'])
                mycursor.execute(sql, val)

    # Commit the transaction
    mydb.commit()