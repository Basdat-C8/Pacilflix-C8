from django.urls import path
from .views import show_daftar_favorit

app_name = 'daftarfavorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit'),
]