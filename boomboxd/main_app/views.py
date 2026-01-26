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
    tracks = topTracks(request)
    return render(request, "home.html", {"avatar": avatar, "albums": tracks})

def topTracks(request):
    playlist_id = '2Md6zqbq1Rb4akJ4HFugWd'
    tracks = sp.playlist(playlist_id)
    return tracks['tracks']['items']

def albumDetail(request, album_id):
    data = sp.album(album_id)
    return render(request, "album-detail.html", {"album": data})


def search(request):
    query = request.POST.get("query")
    data = sp.search(q=query, type='album')
    return render(request, "home.html", {"albums": data['albums']['items'], "query": query})

class createMixtape(CreateView):
    model = Mixtape
    fields = ["title"]
    template_name = "Mixtape_form.html"
