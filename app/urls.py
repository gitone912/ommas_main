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
    path('quality_monitor_data/',quality_monitor_data, name='quality_monitor_data'),
    path('upload/',upload_data, name='upload'),
    path('joint_inspection/',joint_inspection_cnn, name='joint_inspection'),
    path('usfg/',usfg, name='usfg'),
    path('mga/',mga, name='mga'),
    path('report_nlp/',report_nlp, name='nlp_report'),
    path('monitors/',monitors,name='monitors'),
    path('monitors_sqm',monitors_sqm,name='monitors_sqm'),
    path('discrepancies/', disrepancies, name='disc'),
    
]
