from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from favorite.views import  delete_favorit, delete_tayangan_favorit, show_favorite, show_list_favorite

app_name = 'favorite'

urlpatterns = [
    path('detail/<str:timestamp>', show_favorite, name='show_favorite'),
    path('', show_list_favorite , name='show_list_favorite'),
    path('delete/<str:id_tayangan>/<str:timestamp>', delete_tayangan_favorit, name='delete_tayangan_favorit'),
    path('deleteList/<str:timestamp>', delete_favorit, name='delete_favorit')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)