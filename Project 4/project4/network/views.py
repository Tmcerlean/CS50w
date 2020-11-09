from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.utils import timezone
import pytz
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile, Like


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by("timePosted").reverse()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='/login')
def newPost(request):
    if request.method == "POST":
        post = Post()
        post.user = request.user
        post.postContent = request.POST.get("post")
        unformatteddt = timezone.now()
        post.timePosted = unformatteddt
        post.save()
        return render(request, "network/index.html")
    return render(request, "network/index.html")


def profile(request, username):
    loggedInUser = request.user
    profileUser = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profileUser).order_by("timePosted").reverse()
    nofollowers = Profile.objects.filter(user=profileUser, following='').count()
    nofollowing = Profile.objects.filter(user=profileUser, followers='').count()
    if request.user.username and request.user.username != profileUser:
        try:
            Profile.objects.get(user=request.user, following=profileUser)
            currentlyFollowing = True
        except:
            currentlyFollowing = False
    return render(request, "network/profile.html", {
        "loggedInUser": loggedInUser,
        "profileUser": profileUser,
        "posts": posts,
        "currentlyFollowing": currentlyFollowing,
        "nofollowers": nofollowers,
        "nofollowing": nofollowing
    })


@login_required(login_url='/login')
def follow(request, username):
    if request.user.username:
        loggedInUser = request.user
        profileUser = get_object_or_404(User, username=username)
        # Add new follow to logged in user
        newfollow = Profile()
        newfollow.user = loggedInUser
        newfollow.following = profileUser
        newfollow.save()
        # Add new follower to profile viewed
        newfollower = Profile()
        newfollower.user = profileUser
        newfollower.followers = loggedInUser
        newfollower.save()
        return redirect("profile",username=username)
    else:
        return redirect("index.html")


@login_required(login_url='/login')
def unfollow(request, username):
    if request.user.username:
        # Remove follow for logged in user
        profileUser = get_object_or_404(User, username=username)
        unfollow = Profile.objects.get(user=request.user, following=profileUser)
        unfollow.delete()
        # Remove follower from profile viewed
        unfollower = Profile.objects.get(user=profileUser, followers=request.user)
        unfollower.delete()

        return redirect("profile",username=username)
    else:
        return redirect("index.html")


@login_required(login_url='/login')
def following(request, username):
    username = username
    # Create empty posts list
    posts = []
    # Get list of accounts user is following
    accountsFollowing = Profile.objects.filter(followers=request.user)
    # Iterate through list of followed accounts
    for user in accountsFollowing:
    # Get list of posts for account
        accountsPosts = Post.objects.filter(user=user.user)
        # Iterate through posts and append to empty posts list
        for post in accountsPosts:
            posts.append(post)
    # Order list by time posted
    posts.reverse()
    # Paginate posts in groups of 10
    paginatedPosts = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginatedPosts.get_page(page_number)
    return render(request, "network/following.html", {
        "username": request.user.username,
        "accountsFollowing": accountsFollowing,
        "posts": posts,
        "page_obj": page_obj
    })
      

@login_required(login_url='/login')
def editpost(request):
    # Check that request was POST
    if request.method == 'POST':
        # Convert from byte to dict format
        body: dict = json.loads(request.body)  
        # Extract values from dict
        postId: int = body['postId']
        postContent: str = body['postContent']
        try:
            # Access the post with the passed in id
            editedPost = Post.objects.get(id=postId)
            # Update the post content with the passed in content
            editedPost.postContent = postContent
            # Save the post
            editedPost.save()
            # Return a HttpResponse object
            return HttpResponse('Post successfully edited')
        except:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)


@login_required(login_url='/login')
def like(request):
    pass