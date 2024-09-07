import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN_ROLE= config.get('IAM_ROLE','ARN_ROLE')
print(ARN_ROLE)

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
    registration    TIMESTAMP,
    sessionId       INTEGER,
    song            VARCHAR(256),
    status          INTEGER,
    ts              TIMESTAMP,     
    userAgent       VARCHAR(256),
    userId          VARCHAR(50)
);


""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
    artist_id        VARCHAR(256),
    artist_latitude  FLOAT,
    artist_location  VARCHAR(256),
    artist_longitude FLOAT,
    artist_name      VARCHAR(256),
    duration         FLOAT,
    num_songs        INT,
    song_id          VARCHAR(256),
    title            VARCHAR,
    year             INT
);
""")

# FACT TABLE

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay(
    songplay_id INT PRIMARY KEY,     
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

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM 's3://udacity-dend/log_data'
CREDENTIALS 'aws_iam_role={}'
compupdate off
FORMAT AS JSON 's3://udacity-dend/log_json_path.json'
TIMEFORMAT 'epochmillisecs'
REGION 'us-west-2';
""").format(ARN_ROLE)

staging_songs_copy = ("""
COPY staging_songs 
FROM 's3://udacity-dend/song_data/A/B' 
CREDENTIALS 'aws_iam_role={}'  
FORMAT AS JSON 'auto' 
compupdate off 
REGION 'us-west-2';
""").format(ARN_ROLE)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplay (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT 
    ROW_NUMBER() OVER (ORDER BY se.ts) AS songplay_id,
    se.ts AS start_time,
    se.userId::INTEGER AS user_id,
    se.level AS level,
    ss.song_id AS song_id,
    ss.artist_id AS artist_id,
    se.sessionId AS session_id,
    se.location AS location,
    se.userAgent AS user_agent
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT 
    se.userId::INTEGER AS user_id,
    se.firstName as first_name,
    se.lastName as last_name,
    se.gender as gender,
    se.level as level  
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title
WHERE se.page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT 
    ss.song_id as song_id,
    ss.title as title,
    ss.artist_id as astist_id,
    ss.year as year, 
    ss.duration as duration
FROM staging_songs ss
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT
    ss.artist_id as astist_id,
    ss.artist_name as name,
    ss.artist_location as location,
    ss.artist_latitude as latitude,
    ss.artist_longitude as longitude
FROM staging_songs ss
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT 
    se.ts AS start_time,
    EXTRACT(hour FROM se.ts) AS hour,
    EXTRACT(day FROM se.ts) AS day,
    EXTRACT(week FROM se.ts) AS week,
    EXTRACT(month FROM se.ts) AS month,
    EXTRACT(year FROM se.ts) AS year,
    EXTRACT(dow FROM se.ts) AS weekday
FROM staging_events se;
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, staging_events_table_drop, staging_songs_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
