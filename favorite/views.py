from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import connection, InternalError
from datetime import datetime  
from django.urls import reverse
from django.contrib import messages

def show_list_favorite(request):
    # username =  request.session['username'] 
    cursor = connection.cursor()
    print("testttt")
    query = f"""
        SELECT f.judul, f.timestamp
        FROM daftar_favorit f
        WHERE username = 'ashepherdsond'; 
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    favorite = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            if isinstance(value, bytes):
                value = value.decode() 
            detail[attr] = value
        favorite.append(detail)

    context = {
        'favorite': favorite
    }
    print(favorite)
    return render (request, 'list_fav.html',context)

def show_favorite(request, timestamp):
    # username =  request.session['username']
    if timestamp == 'styles.css':
        print("1test")
        return HttpResponse(status=404) 
    print("2test")
    try:
        timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return HttpResponseBadRequest("Invalid timestamp format")
    cursor = connection.cursor()
    query = f"""
        SELECT t.judul AS judul_tayangan, d.judul AS judul_daftar_favorit , f.id_tayangan, f.timestamp
        FROM tayangan_memiliki_daftar_favorit f, tayangan t, daftar_favorit d
        WHERE f.id_tayangan = t.id AND d.username = 'ashepherdsond' AND f.timestamp= '{timestamp_dt}' AND d.timestamp = '{timestamp_dt}'; 
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    print(query)
    res = parse(cursor)
    list_favorite = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            if isinstance(value, bytes):
                value = value.decode()
            detail[attr] = value
        print(detail)
        list_favorite.append(detail)
        judul = list_favorite[0]["judul_daftar_favorit"]
    context = {
        'list_favorite': list_favorite,
        'judul': judul,
    }
    print(list_favorite)
    return render (request, 'list_tayangan_fav.html',context)


def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def delete_favorit(request, timestamp ):
    cursor = connection.cursor()
    query = f"""
    DELETE FROM DAFTAR_FAVORIT
    WHERE username = 'ashepherdsond' AND timestamp={timestamp} ;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    response = HttpResponseRedirect(reverse('favorite:show_list_favorite'))
    return response


def delete_tayangan_favorit(request, id_tayangan, timestamp ):
    cursor = connection.cursor()
    query = f"""
    DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT
    WHERE username = 'ashepherdsond' AND id_tayangan='{id_tayangan}' AND timestamp='{timestamp}' ;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    return  HttpResponseRedirect(reverse('favorite:show_favorite', kwargs={'timestamp': timestamp}))