from django.urls import path
from .views import show_daftar_favorit, get_all_users_daftar_favorit, delete_daftar_favorit, show_daftar_favorit_tayangan

app_name = 'daftarfavorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit'),
    path('user', get_all_users_daftar_favorit, name='show_all_users_daftar_favorit'),
    path('delete', delete_daftar_favorit, name='delete'),
    path('show-tayangan/<str:timestamp>/', show_daftar_favorit_tayangan, name='show_daftar_favorit_tayangan'),
    # path('delete-tayangan', delete_daftar_favorit, name='delete_tayangan'),
]