from django.contrib import admin
from django.urls import path

from download.views import delete_download, show_download

app_name = 'download' #id_tayangan, timestamp

urlpatterns = [
    path('', show_download, name='show_download'),
    path('delete/<str:id_tayangan>/<str:timestamp>', delete_download, name='delete_download'),
]
