from django.contrib import admin

# Register your models here.
from .models import auction_listings, bids, comments

admin.site.register(auction_listings)
admin.site.register(bids)
admin.site.register(comments)