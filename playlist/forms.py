from django import forms
from django.forms import DateInput
from .models import Playlist, PlaylistTrack
from datetime import date

class PlaylistForm(forms.ModelForm):
    ysnFavorite = forms.BooleanField(required=False)

    class Meta:
        model = Playlist
        exclude = ['klngPlaylistID']
        widgets = {
            'strPlaylistDate': DateInput(attrs={'type': 'date'}),
        }
        # set initial date to today's date
        initial = {
            'strPlaylistDate': date.today(),
        }
        
        
class TrackForm(forms.ModelForm):
    class Meta:
        model = PlaylistTrack
        fields = ['sequence_order']
                              

class PlaylistDeleteForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['strPlaylistName', 'strPlaylistDate', 'memPlaylistDescription']
        
class TrackDeleteForm(forms.ModelForm):
    class Meta:
        model = PlaylistTrack
        fields = ['track']     
        

