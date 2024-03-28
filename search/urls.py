from django.urls import path
from .views import search_movies

urlpatterns = [
    path('', search_movies, name='search_movies'),
]
