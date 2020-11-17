from django.urls import path

from . import views

app_name = 'flightfinder'

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('origin_airport_search/', views.origin_airport_search, name='origin_airport_search'),
    path('flight_search', views.flight_search, name='flight_search'), 
]