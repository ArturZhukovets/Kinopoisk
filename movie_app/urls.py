from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.show_all_movies, name='film'),
    path('movie/<slug:slug>', views.ShowMovieDescription.as_view(), name='movie_description'),
    path('directors', views.ShowAllDirectors.as_view(), name='directors'),
    path('directors/<int:pk>', views.InfoAboutDirector.as_view(), name='director_description'),
    path('actors', views.ShowActors.as_view()),
    path('actors/<int:pk>', views.InfoAboutActor.as_view(), name='actor_description'),
    path('add-movie-form', views.add_movie_form, name='add-movie-form'),

]