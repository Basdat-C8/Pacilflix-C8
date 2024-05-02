from django.urls import path
from tayangan.views import show_tayangan, show_trailer, search_results, show_film_details, show_series_details, \
    show_episode_details, search_results_authenticated

app_name = 'tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_read_tayangan'),
    path('trailer', show_trailer, name='show_read_trailer'),
    path('search_results', search_results, name='search_results'),
    path('search_results_authenticated', search_results_authenticated, name='search_results_authenticated'),
    path('film_details', show_film_details, name='show_film_details'),
    path('series_details', show_series_details, name='show_series_details'),
    path('episode_details', show_episode_details, name='show_episode_details'),
]