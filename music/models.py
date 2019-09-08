from django.db import models
from django.conf import settings
from django.urls import reverse


class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete="CASCADE")
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_art = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + " - " + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=100)
    file = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
