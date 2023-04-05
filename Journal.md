## 10-Mar:
- Created Navbar
- Playlists records can now be created by the user in the model playlist. The playlist in memory from the selection of exercises is still not implemented. 

## 6-Mar:
- Centralized base template into a common app to be used by all apps {% extends 'base.html' %}
- added edit and delete functionalities on the playlist template

## 5-Mar:
- Moved db.sqlite3 to Onedrive for automatic backup
- Created the template playlist_list.html linking to playlist_detail.html

## Backlog
- Create a catalogue column on Tracks(models.Model) and initiate it with IBF. We will use the nomenclature below:
    - Collection of musics: IBF, BSAS, HLB, DCU, MAU
    - Catalogue of exercises: CIMEB-12, CIMEB-18, MINOTAUR-MLP
- playlist_detail.html needs to show all fields and do some lookup on exercise name and music details
- add another columns on model playlists to separate the description from comments
- add labels/tags to the playlist (this may be a bit complex as it may need to be further filtered by author) 
- add exercise_tracks functionality to populate playlists and playlisttracks models -> start by developing just a function def() with a button
- add buttons "edit" and "delete" on templates playlist_list.html and playlist_detail.html
    - I reckon in the end playlist_detail.html will have to incorporate exercise_*.html functionalities
- Create a function to save the playlist into the model (probably better on a new template so the user can enter details for the playlist, such as name, description etc)
- add a mem field on each track of the playlist to allow comments
- give an option to change the order of the tracks on the playlist, e.g. up & down icons.
    - ask ChatGPT if there's a simple way to allow a drag n drop of a table.

## 3-March
- exercise_tracks.html
    - Musics are now playing in a pop-up window
    - label on button {add to playlist} reduced to just {add} to bring rows to 1 line

- exercise_list.html
    - Vivencia lines are now presented in the exercise table
    - Filter by vivencia now working properly with AND instead of OR
    - exercise description expanding and contracting based on a CSS



## 28-Feb:
- Created playlist on http://localhost:8000/exercise_tracks/239
    - Implemented a Button to add the track & exercise to the playlist table
    - Playlist table is updated via Javascript without need for a server trip
    - added button to clear the playlist

## 26-Feb:
- Functional Exercise to Tracks, templates and views.
- Inserted bootstrap for better look & feel


## 25-Feb:  Started working on views 
- http://localhost:8000/exercises/ is functional and allows to filter exercises by line of vivencia and partial name
- Radio buttons allow to select individual exercises
- pagination for every 10 exercises
# MILESTONE ACHIEVED: Exercise and Tracks models operational 
## Tracks(models.Model) Exercises and ExerciseTrack successfully imported from MSSQL MusicDB exTracks
- Log: only one record was not imported from tblTracks: klngTrackID=0, which is used for exercises with no music
- Template import.html now initiates:
    - importing of data from MSSQL 
    - deleting all records on the Tracks model.
- Two log files are created after an import: duplicate_records.csv and null_collumns.csv
- Import rejects duplicates based on klngTrackID as PK
- Import also rejects Null values in key columns (trackID, Title, RefCIMEB, Filename)

NB: This should be enough to continue loading the remaining tables: tblExercises and utblTracksExercises from exTracks. There's quite a bit here to be changed to adapt this to import Kate's files. Some examples of what needs to be done:

- Ideally we don't want to import Kate's files and metadata directly from MSSQL, instead it would be nice to have a more perenial solution to serve as import for other didacta collections. This would be based on a set of music files that this python project can read from and process via Audd for metadata, repeating the existing MSSQL procedure, but using SQLite


## 25-Feb: Fix bugs and finalize Tracks model import from exTracks
- Resolved NULL columns issue on tblTracks by changing the Tracks model to accept null values
- added code to reset the Tracks model. 
- Wrote simplistic CSV log for the import.


## 24-Feb: Started Model creation and data import from exTracks
- Created Models under the music_collcls app 
- On music_collcls\models.py added the function import_data_from_sql to load data from MSSQL MusicDB
- Created the routes on views.py urls.py and a template import.html to run the function import_data_from_sql 

## 23-Feb: Project initiation
From the [workflow recipe](https://dev.to/eklaassen/django-cheat-sheet-4fjd) executed the following:

- Prepare the project directory
- Create the virtual environment
- Install/Upgrade Django
- Install Dependencies
- Create the Django project
- Create the Django app
- Create superuser (Solvay complex pwd)
- Add app to the project settings.py
- Run initial migrations

