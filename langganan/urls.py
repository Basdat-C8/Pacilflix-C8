from django.urls import path
from langganan.views import *

app_name = 'langganan'

urlpatterns = [
    path('', show_langganan, name='show_langganan'),
    path('premium', beli_premium, name='beli_premium'),
    path('standard', beli_standard, name='beli_standard'),
    path('basic', beli_basic, name='beli_basic'),
    path('get-transaction', get_user_transaksi, name='get_user_transaksi'),
]