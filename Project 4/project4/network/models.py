from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postContent = models.TextField()
    timePosted = models.DateTimeField()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.CharField(max_length=64, blank=True)
    following = models.CharField(max_length=64, blank=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postLikeId = models.ForeignKey(Post, on_delete=models.CASCADE)

