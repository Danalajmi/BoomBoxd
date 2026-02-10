from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

Pronouns = (('S', "She/Her"), ('H', "He/Him"), ('T', "They/Them"))

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(default='main_app/static/profile_images/default.jpg', upload_to='main_app/static/profile_images/')
    bio = models.TextField()
    pronouns = models.CharField(max_length=2, choices=Pronouns)
    def __str__(self):
        return self.user.username


class Song(models.Model):
    id = models.CharField(primary_key=True)



class Mixtape(models.Model):
    title = models.CharField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Song)

    def get_absolute_url(self):
        return reverse("mix-detail", kwargs={"pk": self.pk})

class Album(models.Model):
    id = models.CharField(primary_key=True)



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    date = models.DateField(null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album', blank=True)
    albumName = models.CharField(blank=True)
    fav = models.CharField()
    least = models.CharField()
    mention = models.CharField()


class Likes(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
