from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import connection, InternalError
import datetime
from django.urls import reverse
from django.contrib import messages
def show_download(request):
    # username =  request.session['username'] 
    cursor = connection.cursor()
    query = f"""
    SELECT t.judul, u.timestamp, u.id_tayangan
    FROM tayangan_terunduh u
    JOIN tayangan t ON t.id = u.id_tayangan
    WHERE u.username = 'ashepherdsond'
    AND DATE_PART('year', AGE(NOW(), u.timestamp)) = 0
    AND DATE_PART('month', AGE(NOW(), u.timestamp)) = 0
    AND DATE_PART('day', AGE(NOW(), u.timestamp)) < 7;
    """
    cursor.execute('set search_path to public')
    cursor.execute(query)
    res = parse(cursor)
    download = []
    for p in res:
        detail = {}
        for attr, value in p.items():
            if isinstance(value, bytes):
                value = value.decode()
              
            detail[attr] = value
        download.append(detail)
    print("download", download)
    context = {
        'download': download,
        'error_message': ""
    }
    return render (request, 'download.html',context)

def delete_download(request, id_tayangan, timestamp ):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = f"""
        DELETE FROM TAYANGAN_TERUNDUH
        WHERE username = 'ashepherdsond' AND id_tayangan= '{id_tayangan}' AND timestamp= '{timestamp}' ;
        """
        print("testini")
        try:
            cursor.execute('set search_path to public')
            cursor.execute(query)
        except InternalError as e: 
            cursor = connection.cursor()
            query = f"""
            SELECT t.judul, u.timestamp, u.id_tayangan
            FROM tayangan_terunduh u
            JOIN tayangan t ON t.id = u.id_tayangan
            WHERE u.username = 'ashepherdsond'
            AND DATE_PART('year', AGE(NOW(), u.timestamp)) = 0
            AND DATE_PART('month', AGE(NOW(), u.timestamp)) = 0
            AND DATE_PART('day', AGE(NOW(), u.timestamp)) < 7;
            """
            cursor.execute('set search_path to public')
            cursor.execute(query)
            res = parse(cursor)
            download = []
            for p in res:
                detail = {}
                for attr, value in p.items():
                    if isinstance(value, bytes):
                        value = value.decode()
                    
                    detail[attr] = value
                download.append(detail)
            context = {
                'download': download,
                'error_message': "Delete Failed"
            }
            return render(request, 'download.html', context)
        return redirect(reverse('download:show_download'))


def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
