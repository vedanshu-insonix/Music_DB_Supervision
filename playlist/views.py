from django.shortcuts import render, get_object_or_404, redirect

from django import urls
from .models import Playlist, PlaylistTrack
from music_collcls.models import Tracks, ExerciseTrack
from .forms import PlaylistForm, PlaylistDeleteForm, TrackForm
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from datetime import date


class PlaylistDeleteView(DeleteView):
    model = Playlist
    success_url = reverse_lazy('playlist_list')
    template_name = 'playlist/playlist_delete.html'
    
class TrackDeleteView(DeleteView):
    model = PlaylistTrack
    success_url = reverse_lazy('playlist_list')
    template_name = 'playlist/track_delete.html'      

from .forms import PlaylistForm

def playlist_list(request):
    playlists = Playlist.objects.all()
    form = PlaylistForm()
    return render(request, 'playlist/playlist_list.html', {'playlists': playlists, 'form': form})

def track_list(request):
    tracks = PlaylistTrack.objects.all()
    form2 = TrackForm()
    return render(request, 'playlist/playlist_detail.html', {'tracks': tracks, 'form2': form2})


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


def track_edit(request, pk):
    track = get_object_or_404(PlaylistTrack, pk=pk)
    pl_id = track.Playlist
    track_rec = PlaylistTrack.objects.filter(Playlist=pl_id).order_by('sequence_order')
    total_track = len(track_rec)
    form2 = None
    if request.method == 'POST':
        form2 = TrackForm(request.POST, instance=track)
        seq=request.POST.get('sequence_order')
        if int(seq) <= int(total_track):
            old_seq = track.sequence_order
            if int(seq) >= int(old_seq):
                gte_rec = PlaylistTrack.objects.filter(Playlist=pl_id, sequence_order__range = [int(old_seq),int(seq)]).values('id','sequence_order')
                sq = gte_rec
                for i in range(len(sq)):
                    PlaylistTrack.objects.filter(pk=sq[i]['id'], Playlist=pl_id).update(sequence_order=int(sq[i]['sequence_order'])-1)
            if int(seq) <= int(old_seq):
                gte_rec = PlaylistTrack.objects.filter(Playlist=pl_id, sequence_order__range = [int(seq),int(old_seq)]).values('id','sequence_order')
                sq = gte_rec
                for i in range(len(sq)):
                    PlaylistTrack.objects.filter(pk=sq[i]['id'], Playlist=pl_id).update(sequence_order=int(sq[i]['sequence_order'])+1) 
            if form2.is_valid():   
                form2.save()
            return redirect('track_list')
    else:
        form2 = TrackForm(instance=track)
    return render(request, 'playlist/track_edit.html', {'form2': form2})

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
        
