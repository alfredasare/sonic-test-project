from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SongForm
from .models import Album, Song
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']


@login_required
def index(request):
    all_albums = Album.objects.all()
    test = False

    query = request.GET.get("q")
    if query:
        test = True
        all_albums = all_albums.filter(
            Q(album_title__icontains=query) |
            Q(artist__icontains=query) |
            Q(genre__icontains=query)
        ).distinct()

    paginator = Paginator(all_albums, 6)

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': queryset,
    }

    if test is False:
        return render(request, 'music/index.html', context)
    else:
        return render(request, 'music/results.html', context)





# class IndexView(generic.ListView):
#     template_name = 'music/index.html'
#     context_object_name = 'all_albums'
#
#     def get_queryset(self):
#         return Album.objects.all()
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(IndexView, self).dispatch(*args, **kwargs)


# @login_required
# def detail(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     return render(request, 'music/detail.html', {'album': album})


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_art']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlbumCreate, self).dispatch(*args, **kwargs)


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_art']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlbumUpdate, self).dispatch(*args, **kwargs)


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlbumDelete, self).dispatch(*args, **kwargs)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/song_form.html', context)
        song = form.save(commit=False)
        song.album = album
        song.file = request.FILES['file']
        file_type = song.file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
            return render(request, 'music/song_form.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/song_form.html', context)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def albumfavorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': 'Go back and refresh the page'})


def songfavorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': 'Go back and refresh the page'})


