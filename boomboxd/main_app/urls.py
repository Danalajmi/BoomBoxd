
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('albums/<str:album_id>', views.albumDetail, name='album_detail'),
    path('Mixtapes/new', views.createMixtape.as_view(), name='Create_mix'),
    path('search/', views.searchAlbums, name='search'),
    path('searchTracks/', views.searchTracks, name='searchTracks'),
    path('Mixtapes/<int:pk>/', views.mixDetail, name='mix-detail'),
    path('Mixtapes/<int:pk>/add', views.lookup, name='mix-add'),
    path('Mixtapes/<int:pk>/addSong', views.songAdd, name='song-add'),

]
