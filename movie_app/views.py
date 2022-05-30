
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Movie, Director, Actor
from django.db.models import F     # Используется для сортировки, например. В данном случаем F используется для сортировки null'ов
from django.db.models import Sum, Max, Min, Count, Avg
from .forms import MovieForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from django.db.models import Value    #Значение для метода annotate()


def show_all_movies(request):
    """Отображение всех фильмов на главной странице. В Movie.objects.all() Лежит QuerySet
    Пройдясь циклом по QuerySet объекту я вызываю в каждой итерации метод save() тем самым я сохраняю в БД всю инфу с Models
    В данном случае я сохранял поле slug, которое определил в Бд после того как заполнил таблицу. Но после того как я сохранил методом save() все данные,
    цикл for. Разумеется нужно запустить сервер, чтобы все заработало!
    При помощи функции F можно обращаться к столбцу таблицу и производить манипуляции с ним
    aggregate() - позволяет создавать при запросе новые колонки при этом не сохраняя их в базе данных.(полезная штука, но хз где ее применять)
    """
    movies = Movie.objects.order_by(F('year').desc(nulls_last=True))    # Поля со значением null отображаются в конце
    # movies = Movie.objects.annotate(
    #     false_bool=Value(False),  # оборачиваю каждое значение False в класс Value
    #     true_bool=Value(True),  # оборачиваю каждое значение True в класс Value
    #     str_field=Value('hello'),
    #     int_field=Value(100),
    #     new_budget=F('budget') + 100   # обращаюсь к колонке budget и увеличиваю его значение на сто
    # )
    count = movies.count()
    agg = movies.aggregate(Avg("budget"), Min("rating"), Max("rating"))
    #     movie.save()
    return render(request, 'movie_app/movies.html', {
        'movies': movies,
        'agg': agg,
        'count': count
    }
                  )


class ShowMovieDescription(DetailView):
    """Передавать аргумент url'a либо через 'slug', либо 'pk' """
    model = Movie
    context_object_name = 'movie'
    template_name = 'movie_app/description_movie.html'


class ShowAllDirectors(ListView):
    model = Director
    context_object_name = 'directors'
    template_name = 'movie_app/directors_page.html'

    def get_queryset(self):
        """Переопределив родительский метод get_queryset, можно менять содержимое/сортировку объекта из БД """
        query = super().get_queryset()
        query = query.order_by('second_name')
        x = 0
        return query


class InfoAboutDirector(DetailView):
    model = Director
    context_object_name = 'director_inf'
    template_name = 'movie_app/director_info.html'


class ShowActors(ListView):
    template_name = 'movie_app/all_actors.html'
    model = Actor
    context_object_name = 'actors'

    def get_queryset(self):
        """Переопределил метод get_queryset, отсортировав отображение актеров"""
        queryset = super().get_queryset()
        ordered_queryset = queryset.order_by('first_name')
        return ordered_queryset


class InfoAboutActor(View):
    def get(self, request, pk: int):
        actor_inf = Actor.objects.get(id=pk)
        context = {
            'actor_inf': actor_inf
        }
        if actor_inf.actor_gender == 'f':
            actor_inf.actor_gender = 'Женский'
        if actor_inf.actor_gender == 'm':
            actor_inf.actor_gender = 'Мужской'
        return render(request, 'movie_app/actor_info.html', context=context)


def add_movie_form(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('film')
    else:
        form = MovieForm()
    context = {
        'form': form
    }
    return render(request, 'movie_app/add_movie.html', context=context)
