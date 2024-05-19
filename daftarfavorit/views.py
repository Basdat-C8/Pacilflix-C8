from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from .query import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import json

# ========================================= show

def show_daftar_favorit(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("login_register:login"))
    
    context = {'use_navbar2': True, 'username':request.session.get('username')}
    return render(request, 'daftarfavorit_read_delete.html', context)

def show_daftar_favorit_tayangan(request, timestamp):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("login_register:login"))
    
    daftar_favorit = query_get_specific_daftar_favorit(timestamp, username)
    judul_daftar_favorit = daftar_favorit[2]
    
    context = {'use_navbar2': True, 
               'username':request.session.get('username'), 
               'timestamp_daftar_favorit':timestamp,
               'judul_daftar_favorit':judul_daftar_favorit}
    return render(request, 'visit_daftar_favorit.html', context)


# ========================================= get

def get_all_users_daftar_favorit(request):
    username = ''

    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("login_register:login"))
    
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
        return HttpResponseRedirect(reverse("login_register:login"))
    
    get_tayangan = query_get_tayangan_daftar_favorit(timestamp, username)

    tayangan = []
    for data in get_tayangan:
        tayangan.append({'judul' : data[0],
                            'id_tayangan' : data[1],
                            'timestamp' : data[2],
                            'username': data[3]}
                            )

    return JsonResponse({'tayangan':tayangan})


# ========================================= delete

def delete_daftar_favorit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        timestamp = data.get('timestamp')
        username = data.get('username')
        query_delete_daftar_favorit(timestamp, username)
        return JsonResponse({'message':'success'})

    return HttpResponseNotFound()

def delete_tayangan(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_tayangan = data.get('id_tayangan')
        timestamp = data.get('timestamp')
        username = data.get('username')
        query_delete_tayangan(id_tayangan, timestamp, username)
        return JsonResponse({'message':'success'})

    return HttpResponseNotFound()