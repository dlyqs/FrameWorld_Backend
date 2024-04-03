from django.urls import path
from .views import search_movies, search_video_bili

urlpatterns = [
    path('', search_movies, name='search_movies'),
    path('video_bili/', search_video_bili, name='search_video_bili'),
]
