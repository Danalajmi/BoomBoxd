
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('albums/', views.albums, name='albums'),
    path('artists/', views.artists, name='arists'),
    path('albums/<int:album_id>', views.albumDetail, name='album_detail')
]
