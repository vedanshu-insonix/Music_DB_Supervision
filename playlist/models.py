from django.db import models


from music_collcls.models import Tracks, Exercises
class Playlist(models.Model):
    klngPlaylistID = models.AutoField(primary_key=True)
    strPlaylistName = models.CharField(max_length=255, null=True,verbose_name="Playlist Name")
    strPlaylistDate = models.DateTimeField(null=True,                   verbose_name="Playlist Date")
    strPlaylistLocation = models.CharField(max_length=255, null=True, verbose_name="Playlist Location")
    memPlaylistDescription = models.TextField(null=True, verbose_name="Playlist Description")
    strPlaylistType = models.CharField(max_length=255, null=True, choices=[('class', 'Class'), ('workshop', 'Workshop')], verbose_name="Playlist Type")
    ysnFavorite = models.BooleanField(null=True, verbose_name="Favorite")
    strAuthor = models.CharField(max_length=255, null=True, verbose_name="Author")

    class Meta:
        db_table = "Playlists"

class PlaylistTrack(models.Model):
    Playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    sequence_order = models.IntegerField(null=True)
    memUserComment = models.TextField(null=True)

    class Meta:
        db_table = "PlaylistTracks"