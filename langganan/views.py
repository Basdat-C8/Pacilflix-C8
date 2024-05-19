from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from .query import *
from django.utils.timezone import now
from .forms import PaymentForm

def show_langganan(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    context = {'use_navbar2': True, 'username':request.session.get('username')}
    return render(request, 'kelola_langganan.html', context)

def beli_premium(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
     
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            timestamp = now().isoformat()
            # Proses pembayaran dan simpan data ke database jika diperlukan
            return render(request, 'success.html', {'timestamp': timestamp, 'payment_method': payment_method})
    else:
        form = PaymentForm()
    
    context = {'use_navbar2': True, 'username':request.session.get('username'), 'form': form}
    return render(request, 'beli_premium.html', context)

def beli_standard(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            timestamp = now().isoformat()
            # Proses pembayaran dan simpan data ke database jika diperlukan
            return render(request, 'success.html', {'timestamp': timestamp, 'payment_method': payment_method})
    else:
        form = PaymentForm()
    
    context = {'use_navbar2': True, 'username':request.session.get('username'), 'form': form}
    return render(request, 'beli_standard.html', context)

def beli_basic(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            timestamp = now().isoformat()
            # Proses pembayaran dan simpan data ke database jika diperlukan
            return render(request, 'success.html', {'timestamp': timestamp, 'payment_method': payment_method})
    else:
        form = PaymentForm()
    
    context = {'use_navbar2': True, 'username':request.session.get('username'), 'form': form}
    return render(request, 'beli_basic.html', context)

def get_user_transaksi(request):
    username = ''
    try:
        username = request.session.get('username')
        print('user : ',username)
    except:
        return HttpResponseRedirect(reverse("authentication:login_user"))
    
    get_transaksi = query_get_transaksi(username)
    transaksi = []

    for data in get_transaksi:
        transaksi.append({'start_date_time': data[1],
                          'end_date_time': data[2],
                          'nama_paket': data[3],
                          'metode_pembayaran': data[4],
                          'timestamp_pembayaran': data[5],
        })
    
    context = {'use_navbar2': True, 'username':request.session.get('username'), 'transaksi':transaksi}
    return render(request, 'kelola_langganan.html', context)