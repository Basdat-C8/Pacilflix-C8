from django.urls import path
from .views import show_daftar_unduhan, get_all_users_unduhan, delete_unduhan

app_name = 'daftarunduhan'

urlpatterns = [
    path('', show_daftar_unduhan, name='show_daftar_unduhan'),
    path('get-users-unduhan', get_all_users_unduhan, name='get_all_users_unduhan'),
    path('delete', delete_unduhan, name='delete_unduhan'),
]