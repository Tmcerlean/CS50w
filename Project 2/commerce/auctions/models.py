from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class LiveListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    listingid = models.IntegerField()
    image = models.CharField(max_length=100, blank=True, null=True, default=None)

class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    datelisted = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    initialprice = models.IntegerField(default=None)
    currentprice = models.IntegerField()
    image = models.CharField(max_length=200, blank=True, null=True, default=None)

class Bid(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()

class Comment(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    comment = models.CharField(max_length=250)
    time = models.CharField(max_length=64, default=None)

class WatchList(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class ClosedAuction(models.Model):
    seller = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winner = models.CharField(max_length=64)
    winningbid = models.IntegerField()
    dateended = models.CharField(max_length=64)
