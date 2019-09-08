from django.conf.urls import url
from . import views


app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.index, name='index'),

    # /music/12
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /music/12/song/add
    url(r'^(?P<album_id>[0-9]+)/add_song/$', views.create_song, name='song-add'),

    # /music/12/song/delete
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='song-delete'),

    # /music/12/favorite_album
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.albumfavorite, name='favorite-album'),

    # /music/12/favorite_song
    url(r'^(?P<song_id>[0-9]+)/favorite_song/$', views.songfavorite, name='favorite-song'),


    # music/album/add
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album-add'),

    # music/album/2
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # music/album/2/delete
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),

    
]
