from django.contrib import admin
from .models import User, Listing, LiveListing, Bid, Comment, WatchList, ClosedAuction

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(LiveListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(ClosedAuction)