from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_all_movies, name='film'),
    path('movie/<slug:slug_movie>', views.show_one_movie_description, name='movie_description'),

]