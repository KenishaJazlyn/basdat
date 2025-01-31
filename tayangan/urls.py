from django.contrib import admin
from django.urls import path

from tayangan.views import *

app_name = 'tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_tayangan'),
    path('detail/film/<str:id>/', show_detail_film, name='show_detail_film'),
    path('detail/series/<str:id>/', show_detail_series, name='show_detail_series'),
    path('detail/series/<int:idSeries>/<int:idEpisode>/', show_detail_episode, name='show_detail_episode'),
    path('unduh/<str:id>/', unduh_view, name='unduh_view'),
    path('favorit/<str:id>/', favorit_view, name='favorit_view'),
    path('search/', search, name='search'),
]
