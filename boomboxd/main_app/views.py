from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .credentials import *
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

    tracks = topTracks(request)
    # fix this for logged out users
    if request.user.is_authenticated:
        mixtapes = Mixtape.objects.filter(creator = request.user).order_by('-pk')
    else:
        mixtapes = []
    return render(request, "home.html", {"albums": tracks, 'mixtapes': mixtapes})


@login_required
def profile(request):
    mixtapes = Mixtape.objects.filter(creator = request.user)
    return render(request, 'profile.html', {'mixtapes': mixtapes})

def topTracks(request):
    # top 20 tracks playlist id
    playlist_id = '2Md6zqbq1Rb4akJ4HFugWd'
    tracks = sp.playlist(playlist_id)
    return tracks['tracks']['items']

@login_required
def albumDetail(request, album_id):
    data = sp.album(album_id)
    return render(request, "album-detail.html", {"album": data})


def searchTracks(query):
    data = sp.search(q=query, type='track')
    return data['tracks']['items']

def searchAlbums(request):
    query = request.POST.get("query")
    data = sp.search(q=query, type='album')
    return render(request, "album-list.html", {"albums": data['albums']['items'], "query": query})


class createMixtape(LoginRequiredMixin, CreateView):
    model = Mixtape
    fields = ["title"]
    template_name = "Mixtape_form.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


@login_required
def addSong(request, pk):
    query = request.POST.get("query") or 'taylor'
    songs = searchTracks(query)
    print('here4')
    return render(request, 'add_songs.html', {'songs': songs, "query": query, "mix_id": pk,})



class UpdateMix(LoginRequiredMixin, UpdateView):
    model = Mixtape
    fields = ['tracks']
    template_name = 'add_songs.html'


class viewMix(LoginRequiredMixin, DetailView):
    model = Mixtape
    template_name = 'view-mix.html'
