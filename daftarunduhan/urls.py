from django.urls import path
from .views import show_daftar_unduhan

app_name = 'daftarunduhan'

urlpatterns = [
    path('', show_daftar_unduhan, name='show_daftar_unduhan'),
]