from django.contrib import admin
from django.urls import include, path
from login_register.views import login_or_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_or_register, name='login_or_register_home'),  # Set the login_register view as the homepage
    path('login_register/', include('login_register.urls')),
    path('main/', include('main.urls')),  # Assuming you have other URLs under 'main'
]
