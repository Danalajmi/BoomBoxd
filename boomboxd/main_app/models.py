from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(default='main_app/static/profile_images/default.jpg', upload_to='main_app/static/profile_images/')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

