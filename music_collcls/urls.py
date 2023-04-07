# urls.py at the app level
from django.urls import path
from . import views
from .views import serve_file


urlpatterns = [
    
    path('save-playlist/<int:tracks>', views.save_playlist, name='save'),
    path('createe/', views.playlist_createe, name='playlist_createe'),
    path('import/', views.import_view, name='import'),
    path('exercises/', views.exercises_list, name='exercises_list'),
    path('exercise_tracks/<int:exercise_id>', views.exercise_tracks, name='exercise_tracks'),
    # path('add_track_to_playlist/<int:track_id>/', views.add_track_to_playlist, name='add_track_to_playlist'),
    path('files/<path:file_path>/', serve_file, name='serve_file'),
    path('', views.home, name='home'),
   
]
