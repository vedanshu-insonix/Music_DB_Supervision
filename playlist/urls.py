from django.urls import path
from . import views
from .views import PlaylistDeleteView, TrackDeleteView

urlpatterns = [
    path('', views.playlist_list, name='playlist_list'),
    path('', views.track_list, name='track_list'),
    path('create/', views.playlist_create, name='playlist_create'),
    path('<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('<int:pk>/edit/', views.playlist_edit, name='playlist_edit'),
    path('<int:pk>/editt/', views.track_edit, name='track_edit'),
    path('<int:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('<int:pk>/deletee/', TrackDeleteView.as_view(), name='track_delete'),
    path('add_tracks/<int:track_id>', views.add_tracks, name='add_tracks'),
]
