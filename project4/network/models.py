from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usersPosts')
    body = models.TextField()
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)