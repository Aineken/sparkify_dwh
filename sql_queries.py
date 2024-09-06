import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN= config.get('IAM_ROLE','ARN')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay CASCADE"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist          VARCHAR(256),
    auth            VARCHAR(50),
    firstName       VARCHAR(50),
    gender          VARCHAR(10),
    itemInSession   INTEGER,
    lastName        VARCHAR(50),
    length          FLOAT,
    level           VARCHAR(10),
    location        VARCHAR(256),
    method          VARCHAR(10),
    page            VARCHAR(50),
    registration    BIGINT,
    sessionId       INTEGER,
    song            VARCHAR(256),
    status          INTEGER,
    ts              BIGINT,     
    userAgent       VARCHAR(256),
    userId          VARCHAR(50)
);


""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
    num_songs        INT,
    artist_id        VARCHAR(256),
    artist_latitude  FLOAT,
    artist_longitude FLOAT,
    artist_location  VARCHAR(256),
    artist_name      VARCHAR(256),
    song_id          VARCHAR(256),
    title            VARCHAR(256),
    duration         FLOAT,
    year             INT
);
""")

# FACT TABLE

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay(
    songplay_id SERIAL PRIMARY KEY,     
    start_time TIMESTAMP NOT NULL,      
    user_id INT NOT NULL,               
    level VARCHAR(10) NOT NULL,
    song_id VARCHAR(20),                
    artist_id VARCHAR(20),              
    session_id INT NOT NULL,
    location VARCHAR(256),
    user_agent VARCHAR(256),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT fk_song FOREIGN KEY (song_id) REFERENCES songs (song_id),
    CONSTRAINT fk_artist FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
    CONSTRAINT fk_time FOREIGN KEY (start_time) REFERENCES time (start_time)

);
""")
# DIMENTION TABLE
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id INT PRIMARY KEY, 
first_name VARCHAR(50), 
last_name VARCHAR(50), 
gender VARCHAR(10), 
level VARCHAR(10) NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
song_id VARCHAR(20) PRIMARY KEY, 
title VARCHAR(256), 
artist_id VARCHAR(20) NOT NULL, 
year INT , 
duration FLOAT NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id VARCHAR(20) PRIMARY KEY, 
name VARCHAR(256), 
location VARCHAR(256), 
latitude FLOAT, 
longitude FLOAT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
    start_time TIMESTAMP PRIMARY KEY,  
    hour INT NOT NULL,                 
    day INT NOT NULL,                 
    week INT NOT NULL,                
    month INT NOT NULL,              
    year INT NOT NULL,             
    weekday VARCHAR(10) NOT NULL       
);
""")


create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

# STAGING TABLES

staging_events_copy = ("""   
COPY staging_events
FROM 's3://udacity-dend/log_data'
CREDENTIALS 'aws_iam_role=<YOUR_IAM_ROLE>'
gzip delimiter ';' 
compupdate off
FORMAT AS JSON 's3://udacity-dend/log_json_path.json'
REGION 'us-west-2'
TIMEFORMAT AS 'epochmillisecs';
""").format(ARN)

staging_songs_copy = ("""
 COPY staging_songs 
 FROM 's3://udacity-dend/song_data' 
CREDENTIALS 'aws_iam_role={}' 
gzip delimiter ';' 
compupdate off 
REGION 'us-west-2';
""").format(ARN)

# FINAL TABLES

songplay_table_insert = ("""

""")

user_table_insert = ("""

""")

song_table_insert = ("""

""")

artist_table_insert = ("""

""")

time_table_insert = ("""

""")

# QUERY LISTS

copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
