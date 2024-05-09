from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def show_daftar_favorit(request):
    context = {'use_navbar2': True}
    return render(request, 'daftarfavorit_read_delete.html', context)
