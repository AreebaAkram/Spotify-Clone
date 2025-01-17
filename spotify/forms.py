from django import forms
from .models import song

class EditSongForm(forms.ModelForm):
    class Meta:
        model = song
        fields = ('title', 'song_image')