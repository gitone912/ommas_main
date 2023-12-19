from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("bot/", bot, name="bot"),
    path('dashboard/',dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('',login_view, name='login'),
    path('map/',map, name='map'),
    path('get_coordinates/',get_coordinates, name='get_coordinates'),

    
]
