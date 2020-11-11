from django.urls import path

from . import views

app_name = 'flightfinder'

urlpatterns = [
    path('', views.index, name='index'),
    path('origin_airport_search/', views.origin_airport_search, name='origin_airport_search')
]