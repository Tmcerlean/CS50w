import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from amadeus import Client, ResponseError, Location

from .models import Airport, Flight, Passenger

# Create your views here.
def index(request):
    return render(request, 'flightfinder/index.html')


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