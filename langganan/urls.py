from django.contrib import admin
from django.urls import path

from langganan.views import show_langganan, show_beli

app_name = 'langganan'

urlpatterns = [
    path('', show_langganan, name='show_langganan'),
    path('beli/<int:id>/', show_beli, name='show_beli')
]
