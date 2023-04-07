from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from functools import reduce
from operator import and_
from playlist.forms import PlaylistForm
from playlist.models import Playlist
from datetime import date

from datetime import timedelta
import pyodbc
import os
import csv

from .models import Tracks, ExerciseTrack, Exercises


def home(request):
    return render(request, 'home.html')

def import_view(request):
    success = False
    deleted = False

    if request.method == 'POST':
        if 'import_tracks_data' in request.POST:
            import_data_from_sql()
            tracks_success = True
        elif 'import_exercises_data' in request.POST:
            import_exercise_data_from_sql()
            exercises_success = True
        elif 'import_tracksexercises_data' in request.POST:
            import_exercise_tracks()
            exercise_track_success = True
        elif 'delete_tracks' in request.POST:
            delete_tracks()
            deleted = True

    return render(request, 'import.html', {'success': success, 'deleted': deleted})

def exercises_list(request):
    exercises_list = Exercises.objects.all().order_by('strExerciseEN')

    # Apply search filter if present
    search_query = request.GET.get('search')
    if search_query:
        exercises_list = exercises_list.filter(Q(strExerciseEN__icontains=search_query))

    # Apply line filter if present
    lines_filter = request.GET.getlist('line')
    if lines_filter:
        lines_filter = [line.upper() for line in lines_filter if line.upper() in ('V', 'S', 'C', 'A', 'T')]
        if lines_filter:
            exercises_list = exercises_list.filter(
                 reduce(and_, [Q(**{'ysnLine{}__in'.format(line): [True]}) for line in lines_filter])
            )


    # Pagination
    paginator = Paginator(exercises_list, 10) # 10 exercises per page
    page = request.GET.get('page')
    exercises = paginator.get_page(page)

    return render(request, 'exercises_list.html', {'exercises': exercises,  'search_query': search_query, 'lines_filter': lines_filter})

from django.http import FileResponse
from django.conf import settings
from playlist.models import Playlist, PlaylistTrack
import os


def serve_file(request, file_path):
    file_full_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, file_path.replace('/', os.sep)))
    return FileResponse(open(file_full_path, 'rb'))

def exercise_tracks(request, exercise_id):
    # get the exercise object and the tracks associated with it
    exercise = get_object_or_404(Exercises, pk=exercise_id)
    exercise_tracks = exercise.exercisetrack_set.all().select_related('track').order_by('track__strTrackTitle') 

    # retrieve the playlist if it exists in memory, otherwise create it
    try:
        playlist = Playlist.objects.get(strPlaylistName='My Playlist')
    except Playlist.DoesNotExist:
        playlist = Playlist.objects.create(strPlaylistName='My Playlist', strAuthor='User')
    tId = request.GET.get('t', ' ')
    if tId != ' ' and tId != 'clear':
        filter_playlist = PlaylistTrack.objects.filter(Playlist=playlist.klngPlaylistID)
        lenPlaylist = len(filter_playlist) + 1
        exId = ExerciseTrack.objects.filter(track=tId)
        exercise = exId[0].exercise
        PlaylistTrack.objects.create(Playlist=Playlist.objects.get(strPlaylistName='My Playlist'),track=Tracks.objects.get(klngTrackID=tId),
                                         sequence_order=lenPlaylist,exercise=exercise)
        return redirect(request.path_info)
    if tId == 'clear':
        filter_playlist = PlaylistTrack.objects.filter(Playlist=playlist.klngPlaylistID)
        filter_playlist.delete()
        return redirect(request.path_info)
    playlist_tracks = PlaylistTrack.objects.filter(Playlist=playlist.klngPlaylistID).select_related('track').order_by('sequence_order')
    # create a context dictionary with exercise, tracks and playlist then pass to the template
    context = {
        'exercise': exercise,
        'exercise_tracks': exercise_tracks,
        'playlist_tracks': playlist_tracks,
        'playlist': playlist
    }
    return render(request, 'exercise_tracks.html', context)

# ------ Code block to manipule the playlist object ------ #
def add_track_to_playlist(request, exercise_id):
    exercise = Exercises.objects.get(pk=exercise_id)
    exercise_tracks = exercise.tracks_set.all()
    playlist = Playlist.objects.get(strPlaylistName='My Playlist')
    
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        track = Tracks.objects.get(klngTrackID=track_id)
        # add track to the playlist
        playlist_track = PlaylistTrack.objects.create(Playlist=playlist, track=track, exercise=exercise)
        playlist_track.save()

        context = {
            'exercise': exercise,
            'exercise_tracks': exercise_tracks,
            'playlist': playlist
        }
        return render(request, 'exercise_tracks.html', context)
    
    # return render(request, 'add_track_to_playlist.html', {'exercise': exercise, 'exercise_tracks': exercise_tracks})

# ------ Code block to Import data from SQL Server ------ #

# ------ Code block to Import data from SQL Server ------ #

def save_playlist(request, klngPlaylistID):
    playlist=Playlist.objects.get(pk=klngPlaylistID)
    
    if request.method == 'POST':
        
        name=request.POST.get('strPlaylistName')
        Date=request.POST.get('strPlaylistDate')
        location=request.POST.get('strPlaylistLocation')
        description=request.POST.get('memPlaylistDescription')
        playlist_type=request.POST.get('strPlaylistType')
        favorite=request.POST.get('ysnFavorite')
        author=request.POST.get('strAuthor')
        
        playlist = Playlist.objects.create(strPlaylistName=name, strPlaylistDate=Date, strPlaylistLocation=location, 
                                           memPlaylistDescription=description, strPlaylistType=playlist_type, ysnFavorite=favorite,
                                           strAuthor=author)
        playlist.save()
        
    
def playlist_createe(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save()
            
            plist_id = playlist.klngPlaylistID
            
            myPlaylist = PlaylistTrack.objects.filter(Playlist=Playlist.objects.get(strPlaylistName='My Playlist').klngPlaylistID)
            
            for rec in myPlaylist:
                tId = rec.track.klngTrackID
                filter_playlist = PlaylistTrack.objects.filter(Playlist=plist_id)
                lenPlaylist = len(filter_playlist) + 1
                exId = ExerciseTrack.objects.filter(track=tId)
                exercise = exId[0].exercise
                PlaylistTrack.objects.create(Playlist=Playlist.objects.get(klngPlaylistID=plist_id),track=Tracks.objects.get(klngTrackID=tId),
                                                sequence_order=lenPlaylist,exercise=exercise)
                
            myPlaylist.delete()

            
            #exercise=Exercises.objects.get(pk=exercise_id)
        return redirect('exercises_list')
    else:
        # set initial date to today's date
        initial = {
            'strPlaylistDate': date.today(),
        }
        form = PlaylistForm(initial=initial)
    return render(request, 'playlist_create_from_exercise.html', {'form': form})



def import_data_from_sql():
# imports Tracks data from SQL Server
    # create a connection to the database and a cursor
    myserver = '127.0.0.1,1433'
    myDatabase = 'MusicDB'
    myUsername = 'sa'
    myPassword = os.environ['sql2022a_pwd']
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+myserver+';DATABASE='+myDatabase+';UID='+myUsername+';PWD='+myPassword)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT [klngTrackID]
            ,[strTrackTitle]
            ,(SELECT strArtistName FROM tbl_extArtists A WHERE T.lngArtistID = A.klngArtistID) strArtist
            ,(SELECT strTitle FROM tbl_extAlbums A WHERE T.lngAlbumID = A.klngAlbumID) strAlbum
            ,[strRefTrCIMEB]
            ,[datTrackLength]
            ,[strFile]
            ,[ysnVinyl]
        FROM tblTracks T
    """)

    null_columns = []
    columns_header = ['Warning_description','klngTrackID', 'strTrackTitle', 'strArtist', 'strAlbum', 'strRefTrCIMEB', 'datTrackLength', 'strFile', 'ysnVinyl']
    null_columns_file = open('null_columns.csv', 'w')
    null_columns_writer = csv.writer(null_columns_file)
    null_columns_writer.writerow(columns_header)
    
    duplicate_record_file = open('duplicate_records.csv', 'w')
    duplicate_record_writer = csv.writer(duplicate_record_file)
    duplicate_record_writer.writerow(columns_header)

    for row in cursor.fetchall():
        #  if key columns  are null and skip the row and  write to CSV file 
        if row[0] is None or row[1] is None or row[4] is None :
            warning_message = 'Null values in key columns (trackID, Title, RefCIMEB). Record skipped: '
            null_columns_writer.writerow([warning_message, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
            continue

        if any(value is None for value in row[0:6]):
            warning_message = 'Null values in non-key columns. Record loaded into model: '
            null_columns_writer.writerow([warning_message, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        
        # check if klngTrackID already exists in database
        klngTrackID = row[0]
        if not Tracks.objects.filter(klngTrackID=klngTrackID).exists():
            # calculate the duration of the song in seconds as a timedelta object:
            if row[5] is None:
                duration_secs = None
            else:
                duration_secs = timedelta(minutes=row[5].minute, seconds=row[5].second)

            track = Tracks(
                klngTrackID=row[0],
                strTrackTitle=row[1],
                strArtist=row[2],
                strAlbum=row[3],
                strRefTrCIMEB=row[4],
                durTrackLength=duration_secs,
                strFile=row[6],
                ysnVinyl=row[7]
            )
            track.save()
        else:
            warning_message = 'Duplicate record found. Record skipped:'
            duplicate_record_writer.writerow([warning_message, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        

    # close the CSV files after the loop
    null_columns_file.close()
    duplicate_record_file.close()

def delete_tracks():
    Tracks.objects.all().delete()


def import_exercise_data_from_sql():
    # create a connection to the database and a cursor
    myserver = '127.0.0.1,1433'
    myDatabase = 'MusicDB'
    myUsername = 'sa'
    myPassword = os.environ['sql2022a_pwd']
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+myserver+';DATABASE='+myDatabase+';UID='+myUsername+';PWD='+myPassword)
    cursor = connection.cursor()


    cursor.execute('SELECT klngExerciseID, strRefExCIMEB, strExerciseEN, memDescriptionEN, ysnFilterOn, strExerciseTypeID, ysnLineV, ysnLineS, ysnLineC, ysnLineA, ysnLineT FROM tbl_extExercises')
    rows = cursor.fetchall()
    for row in rows:
        Exercises.objects.update_or_create(
            klngExerciseID=row[0],
            defaults={
                'strRefExCIMEB': row[1],
                'strExerciseEN': row[2],
                'memDescriptionEN': row[3],
                'ysnFilterOn': row[4],
                'strExerciseTypeID': row[5],
                'ysnLineV': row[6],
                'ysnLineS': row[7],
                'ysnLineC': row[8],
                'ysnLineA': row[9],
                'ysnLineT': row[10],
            }
        )


def import_exercise_tracks():
    # create a connection to the database and a cursor
    myserver = '127.0.0.1,1433'
    myDatabase = 'MusicDB'
    myUsername = 'sa'
    myPassword = os.environ['sql2022a_pwd']
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+myserver+';DATABASE='+myDatabase+';UID='+myUsername+';PWD='+myPassword)
    cursor = connection.cursor()


    cursor.execute("SELECT klngExerciseID, klngTrackID, strRefExCIMEB, strRefTrCIMEB, strVersRefExTrCIMEB, ysnFavorite, memUserComment, ysnLineV, ysnLineS, ysnLineC, ysnLineA, ysnLineT, ysnAt1, ysnAt2, ysnAt3, ysnAt5, ysnAtG FROM utbl_extExercisesTracks")

    for row in cursor.fetchall():
        exercise_track = ExerciseTrack(
            exercise_id=row[0],
            track_id=row[1],
            strRefExCIMEB=row[2],
            strRefTrCIMEB=row[3],
            strVersRefExTrCIMEB=row[4],
            ysnFavorite=row[5],
            memUserComment=row[6],
            ysnLineV=row[7],
            ysnLineS=row[8],
            ysnLineC=row[9],
            ysnLineA=row[10],
            ysnLineT=row[11],
            ysnAt1=row[12],
            ysnAt2=row[13],
            ysnAt3=row[14],
            ysnAt5=row[15],
            ysnAtG=row[16],
        )
        exercise_track.save()

