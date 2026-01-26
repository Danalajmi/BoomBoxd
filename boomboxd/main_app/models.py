from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(default='main_app/static/profile_images/default.jpg', upload_to='main_app/static/profile_images/')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Token_Spotify(models.Model):
    user = models.CharField(unique = True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Song(models.Model):
    title = models.CharField()


class Mixtape(models.Model):
    title = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Song)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.CharField()
    date = models.DateField()
    fav = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='fav')
    least = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='least')
    mention = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='mention')
