from django.urls import path
from .views import show_daftar_favorit, get_all_users_daftar_favorit, delete_daftar_favorit

app_name = 'daftarfavorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit'),
    path('user', get_all_users_daftar_favorit, name='show_all_users_daftar_favorit'),
    path('delete', delete_daftar_favorit, name='delete')
]