import mysql.connector
import os


def get_last_fetched_track_index():
       
        try:
            # Establish a connection to the database
            mydb = mysql.connector.connect(
                host=os.getenv("DB_CONNECTION_HOST"),
                user=os.getenv("DB_CONNECTION_USER"),
                password=os.getenv("DB_CONNECTION_PASSWORD"),
                database=os.getenv("DB_CONNECTION_DATABASE")
            )

            mycursor = mydb.cursor()

            # Execute a query to count the number of rows in the Tracks table
            query = "SELECT COUNT(*) FROM Tracks"
            mycursor.execute(query)

            last_track_index = mycursor.fetchone()[0]

            # Close the database connection
            mydb.close()

            return last_track_index

        except Exception as e:
            print(f"Error fetching last track index from the database: {e}")
            return None