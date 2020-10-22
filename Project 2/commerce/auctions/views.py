from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from decimal import Decimal

from .models import User, Listing, LiveListing, Bid, Comment, WatchList, ClosedAuction


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def createlisting(request):
    if request.method == "POST":
        listing = Listing()
        listing.seller = request.user.username
        listing.title = request.POST.get("itemtitle")
        listing.description = request.POST.get("itemdescription")
        unformatteddt = datetime.now()
        formatteddt = unformatteddt.strftime("%d/%m/%y, %H:%M:%S")
        listing.datelisted = formatteddt
        listing.category = request.POST.get("category")
        listing.initialprice = request.POST.get("initialprice")
        listing.currentprice = request.POST.get("initialprice")
        if request.POST.get("imageurl"):
            listing.image = request.POST.get("imageurl")
        else:
            listing.image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
        listing.save()
        return render(request, "auctions/index.html")
    return render(request, "auctions/createlisting.html")


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except:
        return redirect("index.html")
    if request.user.username:
        try:
            WatchList.objects.get(user=request.user.username, listingid=listing_id)
            iteminwatchlist = True
        except:
            iteminwatchlist = False
    else:
        iteminwatchlist = False
    listing = Listing.objects.get(id=listing_id)
    if request.user.username == listing.seller:
        seller = True
    else:
        seller = False
    try:
        comments = Comment.objects.filter(listingid=listing_id)
    except:
        comments = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "iteminwatchlist": iteminwatchlist,
        "seller": seller,
        "comments": comments
    })  
    

@login_required(login_url='/login')
def addwatchlist(request, listing_id):
    if request.user.username:
        watchlist = WatchList()
        watchlist.user = request.user.username
        watchlist.listingid = listing_id
        watchlist.save()
        return redirect("listing",listing_id=listing_id)
    else:
        return redirect("index.html")


@login_required(login_url='/login')
def removewatchlist(request, listing_id):
    if request.user.username:
        watchlist = WatchList.objects.get(user=request.user.username, listingid=listing_id)
        watchlist.delete()
        return redirect("listing",listing_id=listing_id)
    else:
        return redirect("index.html")


@login_required(login_url='/login')
def addbid(request, listing_id):
    if request.user.username:
        try:
            listing = Listing.objects.get(id=listing_id)
        except:
            return redirect("index.html")
        bid = Bid()
        bid.user = request.user.username
        bid.listingid = listing_id
        bid.bid = request.POST.get("addbid")
        if int(bid.bid) > int(listing.currentprice):
            listing.currentprice = bid.bid
            listing.save()
            bid.save()
            response = redirect("listing", listing_id=listing_id)
            response.set_cookie("errorgreen","Bid successful!",max_age=3)
            return response
        else:
            response = redirect("listing", listing_id=listing_id)
            response.set_cookie("error","Bid did not exceed current price!",max_age=3)
            return response
    else:
        return redirect("index.html")


@login_required(login_url='/login')
def closedauction(request, listing_id):
    if request.user.username:
        try:
            listing = Listing.objects.get(id=listing_id)
        except:
            return redirect("index.html")
        try: 
            bid = Bid.objects.get(id=listing_id)
        except:
            return redirect("index.html")
        closedauction = ClosedAuction()
        closedauction.seller = listing.seller
        closedauction.listingid = listing_id
        closedauction.winner = bid.user
        closedauction.winningbid = bid.bid
        unformatteddt = datetime.now()
        formatteddt = unformatteddt.strftime("%d/%m/%y, %H:%M:%S")
        closedauction.dateended = formatteddt
        itemsold = True
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "closedauction": closedauction,
            "itemsold": itemsold
        })  
    else:
        return redirect("index.html")


@login_required(login_url='/login')
def comment(request, listing_id):
    if request.method == "POST":
        unformatteddt = datetime.now()
        formatteddt = unformatteddt.strftime("%d/%m/%y, %H:%M:%S")
        comments = Comment()
        comments.user = request.user.username
        comments.listingid = listing_id
        comments.comment = request.POST.get("comment")
        comments.time = formatteddt
        comments.save()
        return redirect("listing",listing_id=listing_id)
    else :
        return redirect('index')


