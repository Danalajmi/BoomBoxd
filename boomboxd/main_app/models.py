from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(default='main_app/static/profile_images/default.jpg', upload_to='main_app/static/profile_images/')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Song(models.Model):
    id = models.IntegerField(primary_key=True)

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
