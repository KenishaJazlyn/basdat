from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_langganan(request):
    sql_query1 = """
                SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS perangkat
                FROM paket AS p
                JOIN dukungan_perangkat AS dp ON p.nama = dp.nama_paket
                GROUP BY p.nama;
                """

    sql_query2 = """
                SELECT p.nama, t.start_date_time, t.end_date_time, t.metode_pembayaran, date(t.timestamp_pembayaran) AS tanggal_pembayaran, p.harga
                FROM transaction AS t
                LEFT JOIN paket as p ON t.nama_paket = p.nama
                WHERE t.username = 'egannan0';
                """

    sql_query3 = """
                SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS perangkat, t.start_date_time, t.end_date_time
                FROM transaction AS t
                LEFT JOIN paket AS p on p.nama = t.nama_paket
                LEFT JOIN dukungan_perangkat AS dp on p.nama = dp.nama_paket
                WHERE t.end_date_time > NOW()
                AND t.start_date_time <= NOW()
                AND t.username = 'egannan0'
                GROUP BY p.nama, t.start_date_time, t.end_date_time;
                """

    context = {
        'pakets': parse(sql_query1),
        'transactions':  parse(sql_query2),
        'aktif':  parse(sql_query3)
    }

    return render(request, 'langganan.html', context)

def show_beli(request, paket):
    sql_query = f"""
                WITH paket AS (
                    SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS perangkat
                    FROM paket AS p
                    JOIN dukungan_perangkat AS dp ON p.nama = dp.nama_paket
                    WHERE nama = '{paket}'
                    GROUP BY p.nama
                )
                SELECT * FROM paket
                """
    
    return render(request, 'beli.html', {'paket': parse(sql_query)})

@csrf_exempt
def beli(request, paket):
    sql_query = f"""
                INSERT INTO transaction VALUES (
                    'egannan0',
                    CURRENT_DATE,
                    CURRENT_DATE + interval '30 days',
                    '{paket}',
                    '{request.POST.get('metode')}',
                    NOW()
                );
                """
    
    with connection.cursor() as cursor:
        cursor.execute(sql_query)

    return HttpResponseRedirect(reverse('langganan:show_langganan'))

def parse(sql_query):
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]