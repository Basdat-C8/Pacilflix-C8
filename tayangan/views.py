from django.shortcuts import render

from tayangan.models import Tayangan

# Create your views here.
def show_tayangan(request):
    context = {'use_navbar2': True,
               'range': range(10)
               }
    return render(request, "tayangan_read.html", context)

def show_trailer(request):
    context = {'range': range(10)}
    return render(request,"trailer_read.html", context)

def search_results(request):
    return render(request, 'search_results.html')

def show_film_details(request):
    context = {'use_navbar2': True}
    return render(request, "film_details.html", context)

def show_series_details(request):
    context = {'use_navbar2': True}
    return render(request, "series_details.html", context)

def search_results_authenticated(request):
    context = {'use_navbar2': True}
    return render(request, 'search_results_authenticated.html', context)

def show_episode_details(request):
    context = {'use_navbar2': True}
    return render(request, "episode_details.html", context)

def show_daftar_kontributor(request):
    context = {'use_navbar2': True}
    return render(request, "daftar_kontributor_read.html", context)

# def search_results(request):
#     query = request.GET.get('q')
#     if query:
#         search_results = Tayangan.objects.filter(title__icontains=query)
#     else:
#         search_results = Tayangan.objects.none()
#     return render(request, 'search_results.html', {'search_results': search_results})