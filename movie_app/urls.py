from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_all_movies, name='film'),
    path('movie/<slug:slug_movie>', views.show_one_movie_description, name='movie_description'),
    path('directors', views.show_all_directors, name='directors'),
    path('directors/<int:id_director>', views.info_about_director, name='director_description'),
    path('actors', views.show_all_actors),
    path('actors/<int:id_actor>', views.info_about_actor, name='actor_description'),

]