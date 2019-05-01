import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *



def process_song_file(cur, filepath):
	"""
	process_song_file:

    Performs ETL on song data from the million song dataset. 
    This populates the songs and artists tables in the datawarehouse
	"""
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    file_data = df.iloc[0]
    song_data = (file_data.song_id,file_data.title,\
        file_data.artist_id,int(file_data.year),file_data.duration)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (file_data.artist_id,file_data.artist_name,\
        file_data.artist_location,file_data.artist_longitude, file_data.artist_latitude)
    cur.execute(artist_table_insert, artist_data)

    

def process_log_file(cur, filepath):
	"""
	process_log_file:

		Performs ETL on log data from the user activity logs. 
		This populates the time and users and songplays tables in the datawarehouse
	"""
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = df.registration.apply(lambda x: pd.Timestamp.fromtimestamp(float(x)/1000.).replace(microsecond=0))
    
    # insert time data records
    time_df = pd.DataFrame.from_dict({
        "start_time": t,
        "hour": t.dt.hour,
        "day": t.dt.day,
        "week": t.dt.week,
        "month": t.dt.month,
        "year" : t.dt.year
    }) 

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame.from_dict({"user_id":df.userId,"first_name":df.firstName,"last_name":df.lastName,"gender":df.gender})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, (row.user_id,row.first_name,row.last_name,row.gender))
    
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        start_time  = pd.Timestamp.fromtimestamp(float(row.registration)/1000.).replace(microsecond=0)
        
        songplay_data = (row.ts,start_time,int(row.userId),row.level,songid,artistid,row.location,row.userAgent,row.sessionId)
        
        cur.execute(songplay_table_insert, songplay_data)

        

def process_data(cur, conn, filepath, func):
	"""
	process_data:

    	Performs ETL process to populate datawarehouse
	"""
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
