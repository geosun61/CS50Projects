from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    followed = models.ManyToManyField("User",blank=True,related_name="following")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followed": [user.username for user in self.followed.all()],
        }

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey("User",on_delete=models.CASCADE,related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField("User",blank=True,related_name="liked")
    likes = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
            "liked_by": [u.username for u in self.liked_by.all()],
            "likes": self.likes
        }
