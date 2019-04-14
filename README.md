[star_schema]:/images/starschema.png "Million Songs DW Schema Design"
# Datawarehousing the Million Song Dataset
This project extracts JSON logs of user listening sessions on a music streaming application and loads them into a Postgres Datawarehouse. This will allow further analytics and business intelligence on activity of users and their listening patterns.
## Python Dependencies
* glob
* pandas
* psycopg2
* Postgres Database Connection with Database Creation credentials
* Data Files

## Running the ETL Pipeline
Running the pipeline consist of two processes:
1.  Run ```python create_tables.py``` to set up the database warehouse
2.  Run ```python etl.py``` to populate the datawarehouse

## ETL Process
### The Input Data
The input data consists of two datasets which are described as follows:
1. A subset of real song data from the Million Song Dataset: Each file is in JSON format and contains metadata about a song and the artist of that song. The metadata consists of fields such as song ID, artist ID, artist name, song title, artist location, etc. A sample song record is shown below:
```javascript
{"num_songs": 1, "artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null, 
    "artist_longitude": null, "artist_location": "California - LA", "artist_name": "Casual", 
        "song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```

    * see `/data/song_data`
2. Logs of user activity on a purported music streaming application. The data is actually generated using an event generatory. This data captures user activity on the app and stores metadata such as artist name, authentication status, first name,length ,time , ect. A sample of the log data is shown below:
```javascript
{"artist":"N.E.R.D. FEATURING MALICE","auth":"Logged In",
"firstName":"Jayden","gender":"M","itemInSession":0,"lastName":"Fox","length":288.9922,"level":"free",
    "location":"New Orleans-Metairie, LA","method":"PUT","page":"NextSong",
        "registration":1541033612796.0,"sessionId":184,"song":"Am I High (Feat. Malice)",
            "status":200,"ts":1541121934796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"101"}
```

    * see `/data/log_data`

### Datawarehouse Design
#### Fact Tables
##### SongPlays Table
This table tracks the songs played by users on the platform. It tracks the following metadata:
```javascript
{song_play_id, session_id, user_id,start_time,artist_id,location,song_id, agent}
```
#### Dimension Tables
##### Users Table
This table maintains unique user data on users of the platform. This data is collected from the user activity logs. It tracks the following metadata:
```javascript
{user_id, first_name, last_name,gender}
```
##### Songs Table
This table maintains unique song metadata. This data is collected from the Million Songs dataset. It tracks the following metadata:
```javascript
{song_id, artist_id, song_title,duration,year}
```
##### Artists Table
This table maintains unique artist metadata. This data is collected from the Million Songs dataset. It tracks the following metadata:
```javascript
{artist_id,artist_name,artist_location,artist_longitude, artist_latitude}
```
##### Time Table
This table allows time segments of songs played by users. It allows for aggregation on time in dimensions of hour, day, week month, etc. The data is collected from the user activity logs and tracks the following time data:
```javascript
{start_time,hour,day,week,month,year}
```
#### Schema Design
The schema design is shown below:

![star_schema]

### Data Processing and Warehousing
The ETL Process is broken down into two stages:
#### 1. Processing Songs Data
1. Create the database and setup tables as described in the schema
2. Read the songs data and extract artsist and song data

#### 2. Processing User Data
1. Read the user activity (logs) data and extract the users data
2. Extract the time data from the user activity logs: This can be done by generating hour, day, week, month and year information from the registration field of the user log data.
2. Using the song, artist and length fields from the user log data and the Songs and Artists tables, the song_id and artist_id fields can be determined and inserted into the SongPlays table.
4. Other data inserted into the SongPlays table from the user log data include the songId, sessionId, location and agent fields.

## Results
The results of this ETL can be confirmed by running the notebook `test.ipynb`