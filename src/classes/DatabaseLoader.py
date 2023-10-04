import mysql.connector
from dotenv import load_dotenv

import os


class DatabaseLoader:
    """
    A class used to load data from a CSV file into a MySQL database.

    ...

    Methods
    -------
    establish_connection():
        Establishes a connection to the MySQL database.

    insert_user_if_not_exists(mycursor, row):
        Inserts a new user into the Users table if the user does not already exist.

    insert_track_if_not_exists(mycursor, row):
        Inserts a new track into the Tracks table if the track does not already exist.

    insert_artist_if_not_exists(mycursor, artist_id, artist_name):
        Inserts a new artist into the Artists table if the artist does not already exist.

    insert_track_artist_relation_if_not_exists(mycursor, row, artist_id):
        Inserts a new track-artist relation into the TrackArtists table if the relation does not already exist.

    insert_genre_if_not_exists(mycursor, genre):
        Inserts a new genre into the Genres table if the genre does not already exist.

    insert_track_genre_relation_if_not_exists(mycursor, row, genre_id):
        Inserts a new track-genre relation into the TrackGenres table if the relation does not already exist.

    insert_user_track_relation_if_not_exists(mycursor, row):
        Inserts a new user-track relation into the UserTracks table if the relation does not already exist.

    csv_to_db(csv_file):
        Loads data from a CSV file into the MySQL database.
    """

    @staticmethod
    def establish_connection():
        """
        Establishes a connection to the MySQL database.

        Returns
        -------
        mysql.connector.connection_cext.CMySQLConnection
            A connection to the MySQL database.
        """
        load_dotenv()
        return mysql.connector.connect(
            host=os.getenv("DB_CONNECTION_HOST"),
            user=os.getenv("DB_CONNECTION_USER"),
            password=os.getenv("DB_CONNECTION_PASSWORD"),
            database=os.getenv("DB_CONNECTION_DATABASE")
        )

    @staticmethod
    def insert_user_if_not_exists(mycursor, row):
        """
        Inserts a new user into the Users table if the user does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        row : dict
            A dictionary containing the user data.

        Returns
        -------
        None
        """
        sql = "SELECT * FROM Users WHERE user_id = %s"
        val = (row['user_id'],)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            sql = "INSERT INTO Users (user_id, user_name) VALUES (%s, %s)"
            val = (row['user_id'], row['user_name'])
            mycursor.execute(sql, val)

    @staticmethod
    def insert_track_if_not_exists(mycursor, row):
        """
        Inserts a new track into the Tracks table if the track does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        row : dict
            A dictionary containing the track data.

        Returns
        -------
        None
        """
        sql = "SELECT * FROM Tracks WHERE track_id = %s"
        val = (row['track_id'],)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            sql = "INSERT INTO Tracks (track_id, track_name, track_album, track_duration, added_by) VALUES (%s, %s, %s, %s, %s)"
            val = (row['track_id'], row['track_name'], row['track_album'], row['track_duration'], row['user_id'])
            mycursor.execute(sql, val)

    @staticmethod
    def insert_artist_if_not_exists(mycursor, artist_id, artist_name):
        """
        Inserts a new artist into the Artists table if the artist does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        artist_id : str
            The ID of the artist.
        artist_name : str
            The name of the artist.

        Returns
        -------
        None
        """
        if artist_id is None:
            artist_id = "No Artist"
        sql = "SELECT * FROM Artists WHERE artist_id = %s"
        val = (artist_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            sql = "INSERT INTO Artists (artist_id, artist_name) VALUES (%s, %s)"
            val = (artist_id, artist_name)
            mycursor.execute(sql, val)

    @staticmethod
    def insert_track_artist_relation_if_not_exists(mycursor, row, artist_id):
        """
        Inserts a new track-artist relation into the TrackArtists table if the relation does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        row : dict
            A dictionary containing the track data.
        artist_id : str
            The ID of the artist.

        Returns
        -------
        None
        """
        if artist_id is None:
            artist_id = "No Artist"

        sql = "SELECT * FROM TrackArtists WHERE track_id = %s AND artist_id = %s"
        val = (row['track_id'], artist_id)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            sql = "INSERT INTO TrackArtists (track_id, artist_id) VALUES (%s, %s)"
            val = (row['track_id'], artist_id)
            mycursor.execute(sql, val)

    @staticmethod
    def insert_genre_if_not_exists(mycursor, genre):
        """
        Inserts a new genre into the Genres table if the genre does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        genre : str
            The name of the genre.

        Returns
        -------
        int
            The ID of the genre.
        """
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
        return genre_id

    @staticmethod
    def insert_track_genre_relation_if_not_exists(mycursor, row, genre_id):
        """
        Inserts a new track-genre relation into the TrackGenres table if the relation does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        row : dict
            A dictionary containing the track data.
        genre_id : int
            The ID of the genre.

        Returns
        -------
        None
        """
        sql = "SELECT * FROM TrackGenres WHERE track_id = %s AND genre_id = %s"
        val = (row['track_id'], genre_id)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            sql = "INSERT INTO TrackGenres (track_id, genre_id) VALUES (%s, %s)"
            val = (row['track_id'], genre_id)
            mycursor.execute(sql, val)

    @staticmethod
    def insert_user_track_relation_if_not_exists(mycursor, row):
        """
        Inserts a new user-track relation into the UserTracks table if the relation does not already exist.

        Parameters
        ----------
        mycursor : mysql.connector.cursor_cext.CMySQLCursor
            A cursor object used to execute MySQL queries.
        row : dict
            A dictionary containing the user and track data.

        Returns
        -------
        None
        """
        sql = "SELECT * FROM UserTracks WHERE user_id = %s AND track_id = %s"
        val = (row['user_id'], row['track_id'])
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            sql = "INSERT INTO UserTracks (user_id, track_id) VALUES (%s, %s)"
            val = (row['user_id'], row['track_id'])
            mycursor.execute(sql, val)

    @staticmethod
    def csv_to_db(processed_tracks):
        """
        Loads data from the processed_tracks list into the MySQL database.

        Parameters
        ----------
        processed_tracks : list
            A list of tuples containing track information.

        Returns
        -------
        None
        """
        mydb = DatabaseLoader.establish_connection()
        mycursor = mydb.cursor()

        for track_info in processed_tracks:
            (track_id, track_name, track_album, artist_ids, artist_names, 
             track_duration, genres, user_id, user_name) = track_info

            DatabaseLoader.insert_user_if_not_exists(mycursor, {'user_id': user_id, 'user_name': user_name})
            DatabaseLoader.insert_track_if_not_exists(
                mycursor, {
                    'track_id': track_id,
                    'track_name': track_name,
                    'track_album': track_album,
                    'track_duration': track_duration,
                    'user_id': user_id
                }
            )

            for artist_id, artist_name in zip(artist_ids, artist_names):
                DatabaseLoader.insert_artist_if_not_exists(mycursor, artist_id, artist_name)
                DatabaseLoader.insert_track_artist_relation_if_not_exists(mycursor, {'track_id': track_id}, artist_id)

            for genre in genres:
                genre_id = DatabaseLoader.insert_genre_if_not_exists(mycursor, genre)
                DatabaseLoader.insert_track_genre_relation_if_not_exists(mycursor, {'track_id': track_id}, genre_id)

            DatabaseLoader.insert_user_track_relation_if_not_exists(mycursor, {'user_id': user_id, 'track_id': track_id})

        mydb.commit()
        mydb.close()
        print("Data loaded successfully!")
