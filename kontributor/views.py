from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

# Create your views here.
def show_kontributor(request):
    return render(request, 'kontributor.html')

def get_kontributor(request, id):
    sql_query = """
                WITH kontributor AS (
                    SELECT
                        c.nama,
                        STRING_AGG(t.tipe, ', ') AS tipe,
                        CASE
                            WHEN c.jenis_kelamin = 0 THEN 'Male'
                            WHEN c.jenis_kelamin = 1 THEN 'Female'
                        END AS jenis_kelamin,
                        c.kewarganegaraan
                    FROM
                        contributors c
                    LEFT JOIN (
                        SELECT id, 'Sutradara' AS tipe FROM sutradara
                        UNION ALL
                        SELECT id, 'Pemain' AS tipe FROM pemain
                        UNION ALL
                        SELECT id, 'Penulis Skenario' AS tipe FROM penulis_skenario
                    ) t ON c.id = t.id
                    GROUP BY
                        c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan
                )
                SELECT * FROM kontributor
                """
    if id == 1:
        sql_query += " WHERE 'Sutradara' = ANY(string_to_array(tipe, ', '));"
    elif id == 2:
        sql_query += " WHERE 'Pemain' = ANY(string_to_array(tipe, ', '));"
    elif id == 3:
        sql_query +=" WHERE 'Penulis Skenario' = ANY(string_to_array(tipe, ', '));"
    else:
        sql_query += ";"

    data = parse(sql_query)
    # print(data)
    return JsonResponse(data, safe=False)

def parse(sql_query):
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]