from playlist.models import Playlist, PlaylistTrack


class PlaylistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # retrieve the playlist if it exists in memory, otherwise create it
        try:
            playlist = Playlist.objects.get(strPlaylistName='My Playlist')
        except Playlist.DoesNotExist:
            playlist = Playlist.objects.create(strPlaylistName='My Playlist', strAuthor='User')

        request.playlist = playlist
        response = self.get_response(request)
        return response

from django.http import JsonResponse
import json

