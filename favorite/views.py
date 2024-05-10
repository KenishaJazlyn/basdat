from django.shortcuts import render

# Create your views here.
def show_favorite(request, id):
    return render(request, 'list_tayangan_fav.html')
def show_list_favorite(request):
    return render(request, 'list_fav.html')