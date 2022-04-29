from django.db.models import QuerySet
from django.contrib import admin
from .models import Movie
"""Регистрируем модель в админке. в Аргументах необходимо передать название модели
Для отображения колонок таблицы в адми панели необходимо создать класс в admin.py в котором с добавлением "Admin"
в название класса, который наследуется от admin.ModelAdmin 
--- class MovieAdmin(admin.ModelAdmin): ---
- list_display = ['', '', ''] - список с названиями полей которые мы хотим видеть"""
# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'currency', 'budget', 'rating_description']
    list_editable = ['rating', 'currency', 'budget']
    ordering = ['-rating', 'name']  # Сортировка
    list_per_page = 10      # Количество элементов, отображаемых на странице.
    actions = ['set_dollars', 'set_euro', 'set_rubles']

    @admin.display(ordering='rating', description='рекомендации') # ДЛЯ ВОЗМОЖНОСТИ СОРТИРОВКИ В АДМИН ПАНЕЛИ. descr= ДЛЯ ОТОБРАЖЕНИЯ НАЗВ. КОЛОНКИ
    def rating_description(self, movie: Movie):
        if movie.rating < 68:
            return "Не рекомендовано к просмотру."
        if movie.rating < 80:
            return "Можно посмотреть! Не пожалеете!"
        return "Обязательно к просмотру!"

    @admin.action(description='Установить валюту DOLLAR')  # Описание в админке
    def set_dollars(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.USD)
        self.message_user(
            request,
            f'Было обновлено {count_updated} записей'
        )

    @admin.action(description='Установить валюту EURO')  # Описание в админке
    def set_euro(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.EURO)
        self.message_user(
            request,
            f'Было обновлено {count_updated} записей'
        )

    @admin.action(description='Установить валюту RUBLES')  # Описание в админке
    def set_rubles(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.RUB)
        self.message_user(
            request,
            f'Было обновлено {count_updated} записей'
        )



#  admin.site.register(Movie, MovieAdmin)  # Заменено декоратором