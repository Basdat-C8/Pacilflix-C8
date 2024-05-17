from django.shortcuts import render, redirect
from django.contrib import messages
from .query import authenticate_user, register_user
from django.contrib.auth import logout

def login_or_register(request):
    return render(request, 'login_or_register.html')

def login_view(request):
    context = {'error': False}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if authenticate_user(username, password):
            request.session['username'] = username  
            return redirect('tayangan:show_read_tayangan') # Redirect ke daftar tayangan
        else:
            context['error'] = True

    return render(request, 'login.html', context)

def register_view(request):
    context = {'error': False}
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        country = request.POST.get('country').strip()

        if not username or not password or not country:
            context['error'] = True
        elif register_user(username, password, country):
            messages.success(request, "Registration successful!")
            return redirect('login_or_register')
        else:
            messages.error(request, "Registration failed. Username may already exist.")
    return render(request, 'register.html', context)


def home(request):
    return render(request, 'home.html')

def dummy(request):
    context = {'use_navbar2': True,
               'username': request.session.get('username')}
    return render(request, 'dummy.html', context)

def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for message in storage:
        storage.used = True

    messages.success(request, "You have successfully logged out.")
    return redirect('login_or_register')
