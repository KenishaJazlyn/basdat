from django.contrib import admin
from django.urls import path

from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_landing, name='landing'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]

