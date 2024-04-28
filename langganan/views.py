from django.shortcuts import render

# Create your views here.
def show_langganan(request):
    return render(request, 'langganan.html')

def show_beli(request, id):
    context = {'nama': 'Premium'}
    if id == 1:
        context = {'nama': 'Standar'}
    elif id == 2:
        context = {'nama': 'Basic'}
    return render(request, 'beli.html', context)