from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages  
import uuid
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection, InternalError

# Create your views here.
def show_landing(request):
    try:
        context = {
            'username': request.session['username']
        } 
        return render(request, 'landing.html', context)
    except: 
        context = {
            'username': 'not found'
        }
        return render(request, 'landing.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        asal_negara = request.POST.get('asal_negara')
        
        cursor = connection.cursor()
        query = f"""
        INSERT INTO PENGGUNA VALUES ('{username}', '{password}', '{asal_negara}');
        """

        try:
            cursor.execute('set search_path to public')
            cursor.execute(query)
            return redirect('tayangan:show_tayangan')
        except InternalError as e: 
            # messages.info(request, str(e.args))
            error_message = str(e.args[0])
            start_index = error_message.find('Username')
            end_index = error_message.find('CONTEXT')
            if start_index != -1:
                # Extract the relevant part of the error message
                error_message = error_message[start_index:end_index]
            messages.info(request, error_message)
    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cursor = connection.cursor()
        query = f"""
        SELECT username, password
        FROM pengguna p
        WHERE p.password = '{password}' AND p.username = '{username}';
        """
        cursor.execute('set search_path to public')
        cursor.execute(query)
        res = parse(cursor)
        
        if len(res) == 1:
            mem = res[0]
            for attr in mem:
                if isinstance(mem[attr], uuid.UUID):
                    request.session[attr] = str(mem[attr])
                else:
                    request.session[attr] = mem[attr]
            return redirect('tayangan:show_tayangan')
        else:
            messages.info(request, "Username atau password tidak valid. Silahkan coba kembali.")
        
        return render(request, 'login.html')
            
    return render(request, 'login.html')

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def logout_user(request):
    request.session['username'] = 'not found'
    response = HttpResponseRedirect(reverse('authentication:landing'))
    return response