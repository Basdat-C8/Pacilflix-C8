from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from .query import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

def show_daftar_favorit(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    context = {'use_navbar2': True, 'username':request.session.get('username')}
    return render(request, 'daftarfavorit_read_delete.html', context)

def show_daftar_favorit_tayangan(request, timestamp):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    daftar_favorit = query_get_specific_daftar_favorit(timestamp, username)
    get_tayangan = query_get_tayangan_daftar_favorit(timestamp, username)
    judul_daftar_favorit = daftar_favorit[2]

    tayangan = []
    for data in get_tayangan:
        tayangan.append({'judul' : data[0],
                         'id_tayangan': data[1],
                                'timestamp' : data[2],
                                'username': data[3]}
                                )
    
    context = {'use_navbar2': True, 
               'username':request.session.get('username'), 
               'judul_daftar_favorit':judul_daftar_favorit,
               'tayangan':tayangan}
    return render(request, 'visit_daftar_favorit.html', context)

def get_all_users_daftar_favorit(request):
    username = ''

    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    get_daftar_favorit = query_get_all_users_daftar_favorit(username)

    daftar_favorit = []
    for data in get_daftar_favorit:
        daftar_favorit.append({'timestamp' : data[0],
                                'username' : data[1],
                                'judul': data[2]}
                                )

    return JsonResponse({'daftar_favorit':daftar_favorit})

def get_tayangan_daftar_favorit(request, timestamp):
    username = ''

    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    get_tayangan = query_get_tayangan_daftar_favorit(timestamp, username)

    tayangan = []
    for data in get_tayangan:
        tayangan.append({'id_tayangan' : data[0],
                                'timestamp' : data[1],
                                'username': data[2]}
                                )

    return JsonResponse({'daftar_favorit':daftar_favorit})

def delete_daftar_favorit(request):
    if request.method == 'POST':
        timestamp = request.POST.get('timestamp')
        username = request.POST.get('username')
        print(timestamp)
        print(username)
        query_delete_daftar_favorit(timestamp, username)
        return HttpResponseRedirect(reverse("daftarfavorit:show_daftar_favorit"))

    return HttpResponseNotFound()