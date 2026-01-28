
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('albums/<str:album_id>', views.albumDetail, name='album_detail'),
    path('Mixtape/new', views.createMixtape.as_view(), name='Create_mix'),
    path('search/<str:type>/', views.search, name='search'),

]
