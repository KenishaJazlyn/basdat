from django.contrib import admin
from django.urls import path

from favorite.views import show_favorite, show_list_favorite

app_name = 'favorite'

urlpatterns = [
    path('detail/<int:id>/', show_favorite, name='show_favorite'),
    path('', show_list_favorite , name='show_list_favorite')
]