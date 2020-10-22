from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist/<int:listing_id>", views.removewatchlist, name="removewatchlist"),
    path("bid/<int:listing_id>", views.addbid, name="addbid"),
    path("closedauction/<int:listing_id>", views.closedauction, name="closedauction"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
