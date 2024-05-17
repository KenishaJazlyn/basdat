from django.contrib import admin
from django.urls import path

from langganan.views import show_langganan, show_beli, beli

app_name = 'langganan'

urlpatterns = [
    path('', show_langganan, name='show_langganan'),
    path('show_beli/<str:paket>/', show_beli, name='show_beli'),
    path('beli/<str:paket>/', beli, name='beli')
]
