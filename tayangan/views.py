from django.shortcuts import render

# Create your views here.
def show_tayangan(request):
    return render(request, 'list_tayangan.html')

def show_detail_film(request, id):
    return render(request, 'detail_film.html')

def show_detail_series(request, id):
    return render(request, 'detail_series.html')

def show_detail_episode(request, idSeries, idEpisode):
    return render(request, 'detail_episode.html')

def search(request):
    query = request.GET.get('q')
    context = {'search_term' : query}
    return render(request, 'search.html', context)