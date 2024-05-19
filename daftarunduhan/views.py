from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from .query import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import json

def show_daftar_unduhan(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    context = {'use_navbar2': True, 'username':request.session.get('username')}
    return render(request, 'daftarunduhan_read_delete.html', context)

# ========================================= get

def get_all_users_unduhan(request):
    username = ''

    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    get_unduhan = query_get_downloaded_tayangan(username)
    unduhan = []
    for data in get_unduhan:
        unduhan.append({'judul':data[0],
                            'id_tayangan' : data[1],
                            'username' : data[2],
                            'timestamp': data[3]}
                            )

    return JsonResponse({'unduhan':unduhan})

# ========================================= delete

def delete_unduhan(request):
    if request.method == 'POST':
        # id_tayangan = request.POST.get('id_tayangan')
        # timestamp = request.POST.get('timestamp')
        # username = request.POST.get('username')

        data = json.loads(request.body)
        id_tayangan = data.get('id_tayangan')
        timestamp = data.get('timestamp')
        username = data.get('username')
        
        operation = query_delete_unduhan(id_tayangan, timestamp, username)

        return JsonResponse({'message':operation})

    return HttpResponseNotFound()