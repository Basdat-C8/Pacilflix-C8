from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def show_langganan(request):
    context = {'use_navbar2': True}
    return render(request, 'kelola_langganan.html', context)

def beli_premium(request):
    context = {'use_navbar2': True}
    return render(request, 'beli_premium.html', context)

def beli_standard(request):
    context = {'use_navbar2': True}
    return render(request, 'beli_standard.html', context)

def beli_basic(request):
    context = {'use_navbar2': True}
    return render(request, 'beli_basic.html', context)