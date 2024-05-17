from django.urls import path
from tayangan.views import show_tayangan, search_results, show_film_details, show_series_details, \
    show_episode_details, show_daftar_kontributor, submit_review_film, submit_review_series, watch_episode

app_name = 'tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_read_tayangan'),
    path('search_results', search_results, name='search_results'),
    path('film_details/<uuid:id_tayangan>/', show_film_details, name='show_film_details'),
    path('series_details/<uuid:id_tayangan>/', show_series_details, name='show_series_details'),
    path('episode_details/<uuid:id_series>/<str:sub_judul>/', show_episode_details, name='show_episode_details'),
    path('daftar_kontributor', show_daftar_kontributor, name='show_daftar_kontributor'),
    path('submit_review_film/<uuid:id_tayangan>/', submit_review_film, name='submit_review_film'),
    path('submit_review_series/<uuid:id_tayangan>/', submit_review_series, name='submit_review_series'),
    path('watch_episode/<uuid:id_series>/', watch_episode, name='watch_episode'),
]