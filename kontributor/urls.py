from django.contrib import admin
from django.urls import path

from kontributor.views import show_kontributor, get_kontributor

app_name = 'kontributor'

urlpatterns = [
    path('', show_kontributor, name='show_kontributor'),
    path('get_kontributor/<int:id>/', get_kontributor, name='get_kontributor')
]
