from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from .credentials import *
from .extras import *
from .models import *
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
import requests


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))



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
    avatar = request.user.profile.avatar
    data = albums(request)

    top_albums = sp.artist_albums("06HL4z0CvFAxyc27GXpf02")

    return render(request, "home.html", {"avatar": avatar, "albums": top_albums['items']})


def albums(request):
    # ! wheres 'all albums' end point?? https://api.deezer.com/chart/0/albums returns only one album
    # TODO change /tracks to /albums, this is only for test or use spotify's api
    url = "https://api.deezer.com/chart/0/tracks"
    response = requests.get(url)
    data = response.json()
    return data["data"]


def allAlbums(request):
    kwarg = "code"
    key = request.GET.get(kwarg)

    token = Token_Spotify.objects.filter(user=key)
    print(key, "token")
    playlist_id = "3cEYpjA9oz9GiPac4AsH4n"
    endpoint = f"/playlist/{playlist_id}"
    response = spotify_request(key, endpoint)
    print(f"response : {response}")
    return HttpResponse("hi")


def artists(request):
    url = "https://api.deezer.com/chart/0/artists"
    response = requests.get(url)
    data = response.json()

    return render(request, "top-artists.html", {"artists": data["data"]})


def albumDetail(request, album_id):
    url = f"https://api.deezer.com/album/{album_id}"
    response = requests.get(url)
    data = response.json()
    return render(request, "album-detail.html", {"album": data})


class createMixtape(CreateView):
    model = Mixtape
    fields = ["title"]
    template_name = "Mixtape_form.html"


def search(request):
    query = request.POST.get("query")
    data = []
    if query:
        url = f"https://api.deezer.com/search?q={query}"
        response = requests.get(url)
        data = response.json()

    return render(request, "home.html", {"albums": data["data"], "query": query})
