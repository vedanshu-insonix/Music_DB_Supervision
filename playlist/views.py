from django.shortcuts import render, get_object_or_404, redirect

from django import urls
from .models import Playlist, PlaylistTrack
from music_collcls.models import Tracks, ExerciseTrack
from .forms import PlaylistForm, PlaylistDeleteForm
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from datetime import date


class PlaylistDeleteView(DeleteView):
    model = Playlist
    success_url = reverse_lazy('playlist_list')
    template_name = 'playlist/playlist_delete.html'

from .forms import PlaylistForm

def playlist_list(request):
    playlists = Playlist.objects.all()
    form = PlaylistForm()
    return render(request, 'playlist/playlist_list.html', {'playlists': playlists, 'form': form})


def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    tracks = PlaylistTrack.objects.filter(Playlist=playlist).select_related('track').order_by('sequence_order')
    return render(request, 'playlist/playlist_detail.html', {'playlist': playlist, 'playlist_tracks': tracks})


def playlist_edit(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    form = None
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('playlist_list')
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'playlist/playlist_edit.html', {'form': form})

def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save()
            return redirect('playlist_list')
    else:
        # set initial date to today's date
        initial = {
            'strPlaylistDate': date.today(),
        }
        form = PlaylistForm(initial=initial)
    return render(request, 'playlist/playlist_create.html', {'form': form})

def add_tracks(request,track_id):
    if request.method == 'GET':
        
        plList = PlaylistTrack.objects.filter(Playlist=track_id).values('track__klngTrackID')
        tracks = Tracks.objects.all().exclude(pk__in=plList)
        tId = request.GET.get('t', ' ')
        if tId != ' ':
            playlist = track_id
            filter_playlist = PlaylistTrack.objects.filter(Playlist=playlist)
            lenPlaylist = len(filter_playlist) + 1
            exId = ExerciseTrack.objects.filter(track=tId)
            exercise = exId[0].exercise
            PlaylistTrack.objects.create(Playlist=Playlist.objects.get(klngPlaylistID=playlist),track=Tracks.objects.get(klngTrackID=tId),
                                         sequence_order=lenPlaylist,exercise=exercise)
            return redirect(request.path_info)
            
    return render(request, 'playlist/playlist_show_track.html', {'tracks': tracks})
        
