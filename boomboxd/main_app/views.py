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
from .credentials import *
from .models import *
from .forms import *
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
import requests


sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
)


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid signup - try again"

    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
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
    return render(request, "profile.html", {"mixtapes": mixtapes})


def topTracks(request):
    # top 20 tracks playlist id
    playlist_id = "2Md6zqbq1Rb4akJ4HFugWd"
    tracks = sp.playlist(playlist_id)
    return tracks["tracks"]["items"]


@login_required
def albumDetail(request, album_id):
    data = sp.album(album_id)
    reviews = Review.objects.filter(album=album_id)

    return render(request, "album-detail.html", {"album": data, "reviews": reviews})


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
    fields = ['title']
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


def mixDetail(request, pk):
    mixtape = Mixtape.objects.get(id=pk)
    songs = []
    for song in mixtape.tracks.all():
        title = sp.track(song.id)
        songs.append(title)

    return render(request, "view-mix.html", {"mixtape": mixtape, "songs": songs})


@login_required
def songAdd(request, pk):
    song_id, _ = Song.objects.get_or_create(id=request.POST.get("song_id"))
    mixTape = Mixtape.objects.get(id=pk)
    mixTape.tracks.add(song_id)

    # TODO: change to this: return redirect('song-add', pk = mixTape.id) raises err idk why
    #! duplicate key value violates unique constraint "main_app_song_pkey", line 118 returns None??
    return redirect("mix-detail", pk=mixTape.id)


def createReview(request, album_id):
    form = ReviewForm(request.POST)

    albumTracks = sp.album_tracks(album_id)
    print(form.errors)
    print(request.POST)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():

            review = form.save(commit=False)
            review.album, _ = Album.objects.get_or_create(id=album_id)
            review.user = request.user
            review.date = timezone.now()
            review.save()
            return redirect("album_detail", album_id=album_id)

    return render(
        request,
        "reviews_form.html",
        {"album_id": album_id, "form": form, "albumTracks": albumTracks["items"]},
    )
