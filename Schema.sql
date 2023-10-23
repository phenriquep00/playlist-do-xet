USE playlist_do_xet;


-- Users table with user_id as primary key
CREATE TABLE Users (
    user_id   VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255)
);

-- Artists table with artist_id as primary key
CREATE TABLE Artists (
    artist_id   VARCHAR(255) PRIMARY KEY,
    artist_name VARCHAR(255) NOT null
);

-- Genres table with genre_id as primary key
CREATE TABLE Genres (
    genre_id   INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL 
);

-- Tracks table with track_id as primary key and added_by as foreign key referencing Users
CREATE TABLE Tracks (
    track_id       VARCHAR(255) PRIMARY KEY,
    track_name     VARCHAR(255) NOT NULL ,
    track_album    VARCHAR(255),
    track_duration INT          NOT NULL,
    added_by       VARCHAR(255) NOT NULL,
    
    FOREIGN KEY (added_by) REFERENCES Users(user_id)
);

-- TrackArtists table for many-to-many relationship between Tracks and Artists
CREATE TABLE TrackArtists (
    track_id  VARCHAR(255),
    artist_id VARCHAR(255),
    
    PRIMARY KEY (track_id, artist_id),
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

-- TrackGenres table for many-to-many relationship between Tracks and Genres
CREATE TABLE TrackGenres (
    track_id VARCHAR(255),
    genre_id INT,
    
    PRIMARY KEY (track_id, genre_id),
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

-- ArtistGenres table for many-to-many relationship between Artists and Genres
CREATE TABLE ArtistGenres (
    artist_id VARCHAR(255),
    genre_id  INT,
    
    PRIMARY KEY (artist_id, genre_id),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

-- UserTracks table for many-to-many relationship between Users and Tracks
CREATE TABLE UserTracks (
    user_id  VARCHAR(255),
    track_id VARCHAR(255),
    
    PRIMARY KEY (user_id, track_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
);
