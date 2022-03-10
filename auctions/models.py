from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE



class User(AbstractUser):
    pass

class auction_listings(models.Model):
    product = models.CharField(max_length=64)
    description = models.TextField(max_length=800)
    image = models.URLField(blank= True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_sellers")
    startingbid = models.DecimalField(decimal_places=2, max_digits=10)
    currentbid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    category = models.CharField(max_length=50, blank= True)
    buyer = models.ForeignKey(User, null= True, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    watchers = models.ManyToManyField(User, blank=True, related_name="all_watchers")

class bids(models.Model):
    listing = models.ForeignKey(auction_listings, on_delete=models.CASCADE)
    offer = models.DecimalField(decimal_places=2, max_digits=10)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)


class comments(models.Model):
    listing = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="get_comments")
    comment = models.CharField(max_length=280)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
