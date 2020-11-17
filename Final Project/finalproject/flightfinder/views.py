import json
from amadeus import Client, ResponseError, Location
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Airport, Flight, Passenger

amadeus = Client(client_id='iSHb849cZ8n5ogZNFs4ifWaG1ErpMp89', 
                 client_secret='5cS9MUKCzyYlBcJ3', 
                 log_level='debug') 

# Create your views here.
def index(request):
    return render(request, 'flightfinder/index.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("Flightfinder:index"))
        else:
            return render(request, 'flightfinder/login.html', {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, 'flightfinder/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("Flightfinder:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["email"]
        email = request.POST["email"]


        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, 'flightfinder/register.html', {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'flightfinder/register.html', {
                "message": "Account already exists."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("Flightfinder:index"))
    else:
        return render(request, 'flightfinder/register.html')

def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None), subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')

def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode']+', '+data[i]['name'])
    result = list(dict.fromkeys(result))
    return json.dumps(result)

def flight_search(request): 
    originFull = request.POST.get('Origin')
    originThree = originFull[:3]
    destinationFull = request.POST.get('Destination')
    destinationThree = destinationFull[:3]
    kwargs = {'originLocationCode': originThree,
            'destinationLocationCode': destinationThree, 
            'departureDate': request.POST.get('Departuredate'), 
            'returnDate': request.POST.get('Returndate'),
            'adults': '1'}
            
    try: 
        response = amadeus.shopping.flight_offers_search.get(
        **kwargs)
        data = []
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        for resp in response.data:
            data.append(resp)
        # Paginate posts in groups of 10
        paginatedFlightResults = Paginator(data, 10)
        page_number = request.GET.get('page')
        page_obj = paginatedFlightResults.get_page(page_number)
        return render(request, "flightfinder/flight_search.html", {
            "data": data,
            "origin": origin,
            "destination": destination,
            "page_obj": page_obj
    })
    except ResponseError as error:
        raise error