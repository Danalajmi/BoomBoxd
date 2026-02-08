
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('albums/<str:album_id>', views.albumDetail, name='album_detail'),
    path('Mixtapes/new', views.createMixtape.as_view(), name='Create_mix'),
    path('Mixtapes/<int:pk>/add', views.lookup, name='mix-add'),
    path('Mixtapes/<int:pk>/update', views.updateMixtape.as_view(), name='mix-update'),
    path('search/', views.searchAlbums, name='search'),
    path('searchTracks/', views.searchTracks, name='searchTracks'),
    path('Mixtapes/<int:pk>/', views.mixDetail, name='mix-detail'),
    path('Mixtapes/<int:pk>/delete', views.DeleteMix.as_view(), name='mix-delete'),
    path('Mixtapes/<int:pk>/addSong', views.songAdd, name='song-add'),
    path('Mixtapes/<int:pk>/removeSong', views.songRemove, name='remove_song'),
    path('reviews/<str:album_id>/add/', views.createReview, name='createReview'),
    path('reviews/remove/<str:album_id>/<str:view>/<int:pk>/', views.DeleteReview.as_view(), name='deleteReview'),

]
