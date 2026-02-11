from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from boomboxd.main_app.models import *
from boomboxd.main_app.forms import *
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
import requests


sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET')
    )
)


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid signup - try again"

    form = UserCreationForm()
    profileForm = ProfileForm()

    context = {"form": form, "error_message": error_message, 'profileForm': profileForm}
    return render(request, "registration/signup.html", context)


def home(request):

    tracks = topTracks(request)
    if request.user.is_authenticated:
        mixtapes = Mixtape.objects.filter(creator=request.user).order_by("-pk")
    else:
        mixtapes = []
    return render(request, "home.html", {"albums": tracks, "mixtapes": mixtapes})


@login_required
def profile(request):
    mixtapes = Mixtape.objects.filter(creator=request.user)
    reviews = Review.objects.filter(user=request.user)

    return render(request, "profile.html", {"mixtapes": mixtapes, "reviews": reviews})


def topTracks(request):
    # top 20 tracks playlist id
    playlist_id = "2Md6zqbq1Rb4akJ4HFugWd"
    tracks = sp.playlist(playlist_id)
    return tracks["tracks"]["items"]


def albumDetail(request, album_id):
    data = sp.album(album_id)

    if request.user.is_authenticated:
        reviews = Review.objects.filter(album=album_id)
        playlist = Likes.objects.get(user=request.user).songs.all()
        liked_ids = {t.id for t in playlist}
    else:
        reviews = []
    return render(request, "album-detail.html", {"album": data, "reviews": reviews, 'liked': playlist, 'liked_ids': liked_ids})


def searchTracks(query):
    data = sp.search(q=query, type="track")
    return data["tracks"]["items"]


def searchAlbums(request):
    query = request.POST.get("query")
    data = sp.search(q=query, type="album")
    return render(
        request, "album-list.html", {"albums": data["albums"]["items"], "query": query}
    )


class createMixtape(LoginRequiredMixin, CreateView):
    model = Mixtape
    fields = ["title"]
    template_name = "Mixtape_form.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class updateMixtape(LoginRequiredMixin, UpdateView):
    model = Mixtape
    fields = ["title"]
    template_name = "Mixtape_form.html"


@login_required
def lookup(request, pk):

    query = request.POST.get("queryTrack")
    if query:
        songs = searchTracks(query)
    else:
        songs = []
        query = ""
    return render(
        request, "add_songs.html", {"songs": songs, "queryTrack": query, "mix_id": pk}
    )


class UpdateMix(LoginRequiredMixin, UpdateView):
    model = Mixtape
    fields = ["tracks"]
    template_name = "add_songs.html"

    def get_success_url(self):
        return reverse("mix-detail", pk=self.object.pk)


def mixDetail(request, pk):
    mixtape = Mixtape.objects.get(id=pk)
    songs = []
    for song in mixtape.tracks.all():
        title = sp.track(song.id)
        songs.append(title)

    return render(request, "view-mix.html", {"mixtape": mixtape, "songs": songs})


@login_required
def songAdd(request, pk):
    mixTape = Mixtape.objects.get(id=pk)
    if request.POST:
        song_id, _ = Song.objects.get_or_create(id=request.POST.get("song_id"))
        mixTape.tracks.add(song_id)
        return redirect('song-add', pk = mixTape.id)

    return render(request, 'add_songs.html', {'mix_id': mixTape.id})


@login_required
def songRemove(request, pk):
    song_id = Song.objects.get(id=request.POST.get("song_id"))

    mixTape = Mixtape.objects.get(id=pk)
    mixTape.tracks.remove(song_id)

    return redirect("mix-detail", pk=mixTape.id)


def createReview(request, album_id):
    form = ReviewForm(request.POST)

    albumTracks = sp.album_tracks(album_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.album, _ = Album.objects.get_or_create(id=album_id)
            review.albumName = sp.album(album_id)['name']
            review.user = request.user
            review.date = timezone.now()
            review.save()
            return redirect("album_detail", album_id=album_id)

    return render(
        request,
        "reviews_form.html",
        {"album_id": album_id, "form": form, "albumTracks": albumTracks["items"]},
    )


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "review_delete_confirm.html"

    def get_success_url(self):

        if self.kwargs.get("view") == "profile":
            return reverse("profile")
        else:

            return reverse(
                "album_detail", kwargs={"album_id": self.kwargs.get("album_id")}
            )


class DeleteMix(LoginRequiredMixin, DeleteView):
    model = Mixtape
    template_name = "mix_delete_confirm.html"

    success_url = "/"


@login_required
def likeSong(request, view):
    song_id, _ = Song.objects.get_or_create(id=request.POST.get("song_id"))
    playlist = Likes.objects.get(user=request.user)
    if song_id in playlist.songs.all():
        playlist.songs.remove(song_id)
    else:
        playlist.songs.add(song_id)
    album_id = sp.track(song_id.id)
    if view == 'profile':
        return redirect('LikedSongs')
    else:
        return redirect('album_detail', album_id['album']['id'])


def listLiked(request):
    playlist = Likes.objects.get(user=request.user)

    songs = playlist.songs.filter(likes=request.user.id).values()
    songList = []
    for song in songs:
        songList.append(sp.track(song["id"]))
    return render(request, "liked.html", {"songs": songList})
