from django.contrib import admin
from django.urls import path

from favorite.views import show_favorite

app_name = 'favorite'

urlpatterns = [
    path('', show_favorite, name='show_favorite')
]
