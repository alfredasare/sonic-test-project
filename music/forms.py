from django import forms
from django.contrib.auth import get_user_model
from music.models import Song


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'file']


class SignUpForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['second_name']
        user.save()
