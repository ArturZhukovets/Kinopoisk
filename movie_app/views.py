
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Movie, Director, Actor
from django.db.models import F     # Используется для сортировки, например. В данном случаем F используется для сортировки null'ов
from django.db.models import Sum, Max, Min, Count, Avg
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


def show_one_movie_description(request, slug_movie: str):
    """get_object_or_404 - Работает как функция get(), но если не передано никакого значения отдаёт response 404"""
    movie = get_object_or_404(Movie, slug=slug_movie)    # Первый аргумент Объект, второй название колонки которую ищем

    return render(request, 'movie_app/description_movie.html', context=
                  {'movie': movie}
                  )


def show_all_directors(request):
    """Создаю views всех режиссёров. Обращаемся к базе, сортируем все объекты по алфавиту, получаем QuerySet, отправляем
    его в context."""
    directors = Director.objects.order_by('second_name')
    context = {
        'directors': directors
    }
    return render(request, 'movie_app/directors_page.html', context=context)


def info_about_director(request, id_director: int):
    """Создаю views с информацией о режиссёре"""
    director_inf = get_object_or_404(Director, id=id_director)
    context = {
        "director_inf": director_inf
    }
    return render(request, 'movie_app/director_info.html', context=context)


def show_all_actors(request):
    actors = Actor.objects.order_by('first_name')
    context = {
        "actors": actors
    }
    return render(request, 'movie_app/all_actors.html', context=context)


def info_about_actor(request, id_actor: int):
    actor_inf = get_object_or_404(Actor, id=id_actor)
    context = {
        "actor_inf": actor_inf
    }
    if actor_inf.actor_gender == 'f':
        actor_inf.actor_gender = 'Женский'
    if actor_inf.actor_gender == 'm':
        actor_inf.actor_gender = 'Мужской'
    return render(request, 'movie_app/actor_info.html', context=context)
