from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    pass

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    outboundDate = models.DateTimeField()
    inboundDate = models.DateTimeField(blank=True, null=True)
    userCountry = models.CharField(max_length=50, default=None)
    userCurrency = models.CharField(max_length=4)
    userLocale = models.CharField(max_length=50, default=None)
    bookingDate = models.DateTimeField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"