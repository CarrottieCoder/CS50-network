from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # The users that are following THIS USER
    # Related name: following, meant THE USER this user follows
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "followers": [follower for follower in self.followers.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usersPosts')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='posts_liked')
    timestamp = models.DateTimeField(auto_now_add=True)

    def count_likes(self):
        return self.likes.count()


    def __str__(self):
        return f"{self.author} posted on {self.timestamp}: {self.body[:50]}"

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }