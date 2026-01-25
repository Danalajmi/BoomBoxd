from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import *
import os
import os
from dotenv import load_dotenv
load_dotenv()
import requests

# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid signup - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def home(request):
    avatar = request.user.profile.avatar
    data = albums(request)
    return render(request, 'home.html', {'avatar': avatar, 'albums': data})


def albums(request):
    # ! wheres 'all albums' end point?? https://api.deezer.com/chart/0/albums returns only one album
    # TODO change /tracks to /albums, this is only for test or use spotify's api
    url = "https://api.deezer.com/chart/0/tracks"
    response = requests.get(url)
    data = response.json()
    return (data['data'])


# def albums(request):
#     clientID = os.getenv(SPOTIFY_CLIENT_ID)



def artists(request):
    url = "https://api.deezer.com/chart/0/artists"
    response = requests.get(url)
    data = response.json()

    return render (request, 'top-artists.html', {'artists': data["data"]})

def albumDetail(request, album_id):
    url = f"https://api.deezer.com/album/{album_id}"
    response = requests.get(url)
    data = response.json()
    return render(request, 'album-detail.html', {'album': data})

class createMixtape(CreateView):
    model = Mixtape
    fields = ['title']
    template_name = 'Mixtape_form.html'


def search(request):
    query = request.POST.get('query')

    print(f'query:::',{request})
    data = []
    if query:
        url = f"https://api.deezer.com/search?q={query}"
        response = requests.get(url)
        data = response.json()

    return render(request, 'home.html', {'albums': data['data']})
