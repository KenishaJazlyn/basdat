from django.contrib import admin
from django.urls import path

from download.views import show_download

app_name = 'download'

urlpatterns = [
    path('', show_download, name='show_download')
]
