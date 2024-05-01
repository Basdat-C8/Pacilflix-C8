# login_register/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from .forms import CustomUserCreationForm  # Assuming this is your form for user registration
from django.contrib import messages

def login_or_register(request):
    # Your existing login_or_register view logic
    return render(request, 'login_or_register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['X'] = True  # Set a custom session variable 'X' upon successful login
            messages.success(request, "Login successful!")  # Optional: Success message
            return redirect('dummy.html')  # Redirect to the 'Daftar Tayangan' page
        else:
            messages.error(request, "Invalid username or password")  # Show an error if login is invalid
            return render(request, 'login.html', {'username': username})
    else:
        return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        # Perform registration logic
        pass  # Replace with code to create a new user and log them in
    else:
        # Just display the registration form
        return render(request, 'register.html')



# def register_view(request):
#     form = CustomUserCreationForm()
#     form_profile = ProfileForm(request.POST or None)

#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid() and form_profile.is_valid():
#             user = form.save()
#             profile = form_profile.save(commit=False)
#             profile.user = user
#             profile.save()
#             messages.success(request, 'Your account has been successfully created!')
#             return redirect('autentifikasi:login')
#     context = {'form': form, 'form_profile': form_profile}
#     return render(request, 'register.html', context)

def home(request):
    # Your existing home view logic, if any
    return render(request, 'home.html')

def dummy(request):
    context = {'use_navbar2': True}  # Context flag to switch navbar
    return render(request, 'dummy.html', context)

