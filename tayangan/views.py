import datetime
from django.db import InternalError, connection
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
import download
from download.views import show_download
from django.contrib.auth.decorators import login_required


# Create your views here.
def show_tayangan(request):
    username = request.session['username']
    context = {'username' : username}
    return render(request, 'list_tayangan.html', context)

def show_detail_film(request, id):
    cursor = connection.cursor()
    username = request.session['username']
    print("testttt")
    query1 = f"""
        SELECT f.judul, f.timestamp
        FROM daftar_favorit f
        WHERE username = '{username}'; 
    """
    cursor.execute('set search_path to public')
    cursor.execute(query1)
    res = parse(cursor)
    favorite = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            if isinstance(value, bytes):
                value = value.decode() 
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')  # Ubah ke format string yang diinginkan
            detail[attr] = value
        favorite.append(detail)

    context = {
        'favorite': favorite,
        'id': id
    }
    
    return render(request, 'detail_film.html', context)

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_detail_series(request, id):
    cursor = connection.cursor()
    username = request.session['username']
    print("testttt")
    query1 = f"""
        SELECT f.judul, f.timestamp
        FROM daftar_favorit f
        WHERE username = '{username}'; 
    """
    cursor.execute('set search_path to public')
    cursor.execute(query1)
    res = parse(cursor)
    favorite = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            if isinstance(value, bytes):
                value = value.decode() 
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')  # Ubah ke format string yang diinginkan
            detail[attr] = value
        favorite.append(detail)

    context = {
        'favorite': favorite,
        'id': id
    }
    return render(request, 'detail_series.html', context)

def show_detail_episode(request, idSeries, idEpisode):
    return render(request, 'detail_episode.html')

def unduh_view(request, id):
    if request.method == 'POST':
        cursor = connection.cursor()
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        query2 = f"""
            INSERT INTO TAYANGAN_TERUNDUH VALUES ('{id}', 'ashepherdsond', '{timestamp}' )
            """      
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query2)
        except InternalError as e: 
            messages.info(request, str(e.args))
        return redirect(reverse('download:show_download'))

def favorit_view(request, id):
    if request.method == 'POST':
        cursor = connection.cursor()
        selected_timestamp = request.POST.get('favoriteListDropdown')
        query = f"""
            INSERT INTO TAYANGAN_MEMILIKI_DAFTAR_FAVORIT  VALUES ('{id}', '{selected_timestamp}','ashepherdsond')
            """  
        print("query ",query)    
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query)
        except InternalError as e: 
            messages.info(request, str(e.args))
        return  HttpResponseRedirect(reverse('favorite:show_favorite', kwargs={'timestamp': selected_timestamp}))

def search(request):
    query = request.GET.get('q')
    context = {'search_term' : query}
    return render(request, 'search.html', context)

