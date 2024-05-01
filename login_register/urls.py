# login_register/urls.py

from django.urls import path
from .views import login_or_register, login_view, register_view,dummy

urlpatterns = [
    path('', login_or_register, name='login_or_register'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dummy/', dummy, name='dummy'),  # Dummy view URL
]
