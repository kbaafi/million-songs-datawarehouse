# DROP TABLES
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES
songplay_table_create = ("""
    create table songplays(
    song_play_id varchar not null,
    start_time timestamp not null,
    user_id int not null,
    level varchar not null,
    song_id varchar,
    artist_id varchar,
    session_id varchar not null,
    location varchar not null,
    user_agent varchar not null,
    primary key(song_play_id,user_id)
    )
""")

user_table_create = ("""
    create table users(
    user_id int primary key not null,
    first_name varchar not null,
    last_name varchar not null,
    gender char(1) not null ) 
""")

song_table_create = (""" 
    create table songs(
    song_id varchar primary key not null,
    song_title varchar not null,
    artist_id varchar not null,
    year int not null,
    duration numeric(12,6) not null) 
""")

artist_table_create = ("""
    create table artists(
    artist_id varchar primary key not null,
    artist_name varchar not null,
    artist_location varchar,
    artist_longitude numeric(11,8),
    artist_latitude numeric(11,8))
""")

time_table_create = ("""
    create table time(
    start_time timestamp primary key not null,
    hour int not null,
    day int not null,
    week int not null,
    month int not null,
    year int not null)
""")

# INSERT RECORDS
songplay_table_insert = ("""
    insert into songplays
    (song_play_id,start_time,user_id,level,song_id,artist_id,
    location,user_agent,session_id)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    on conflict(song_play_id,user_id) 
    do nothing;
""")

user_table_insert = (""" 
    insert into users
    (user_id, first_name,last_name,gender)
    values(%s,%s,%s,%s)
    on conflict(user_id) do update
    set first_name = excluded.first_name,
    last_name = excluded.last_name,
    gender = excluded.gender;
""")

song_table_insert = ("""
    insert into songs
    (song_id,song_title,artist_id,year,duration) 
    values (%s,%s,%s,%s,%s)
    on conflict(song_id) do update
    set song_title = excluded.song_title,
    artist_id = excluded.artist_id,
    year = excluded.year,
    duration = excluded.duration;
""")

artist_table_insert = ("""
    insert into artists
    (artist_id,artist_name,artist_location,artist_longitude, artist_latitude) 
    values (%s,%s,%s,%s,%s)
    on conflict (artist_id) do update
    set artist_name = excluded.artist_name,
    artist_location = excluded.artist_location,
    artist_longitude = excluded.artist_longitude,
    artist_latitude = excluded.artist_latitude
""")


time_table_insert = ("""
    insert into time
    (start_time,hour,day,week,month,year) values
    (%s,%s,%s,%s,%s,%s)
    on conflict(start_time)
    do nothing;
""")

#FIND SONGS
song_select = ("""
    select a.artist_name,s.song_title
    from artists as a, 
    songs as s 
    where 
    a.artist_id = s.artist_id and 
    s.song_title = %s and 
    a.artist_name = %s and 
    s.duration = %s
""")

# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, \
    song_table_create, artist_table_create, time_table_create]

drop_table_queries = [songplay_table_drop, user_table_drop, \
    song_table_drop, artist_table_drop, time_table_drop]