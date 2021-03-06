from django.db.models import QuerySet
from django.contrib import admin
from .models import Movie, Director, Actor, DressingRoom

"""Регистрируем модель в админке. в Аргументах необходимо передать название модели
Для отображения колонок таблицы в адми панели необходимо создать класс в admin.py в котором с добавлением "Admin"
в название класса, который наследуется от admin.ModelAdmin 
--- class MovieAdmin(admin.ModelAdmin): ---
- list_display = ['', '', ''] - список с названиями полей которые мы хотим видеть"""


# Register your models here.


class RatingFilter(admin.SimpleListFilter):
    """Создаю собственный фильтр по рейтингам"""
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating_filter'

    def lookups(self, request, model_admin):
        return [
            ('0-49', 'Низкий'),
            ('50-65', 'Средний'),
            ('66-79', 'Высокий'),
            ('80-100', 'Высочайший'),
        ]

    def queryset(self, request, queryset: QuerySet):
        """В self.value() Подставляется первое значение из кортежа для правильного использования фильтров
        вспоминаем Django ORM filter"""
        if self.value() == '0-49':
            return queryset.filter(rating__lt=50)  # Команды из Django ORM | filter
        if self.value() == '50-65':
            return queryset.filter(rating__gte=50).filter(rating__lt=65)
        if self.value() == '66-79':
            return queryset.filter(rating__gte=66).filter(rating__lt=79)
        if self.value() == '80-100':
            return queryset.filter(rating__gte=79)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Все аргументы данного класса в той или иной форме влияют на отображение
    полей в админке."""
    list_display = ['name', 'rating', 'budget', 'director', 'rating_description']  # отображаются в таблице Movies
    list_editable = ['rating', 'budget', 'director']                                # Позволяет изменять данные
    # fields = ['name', 'rating']  # Поля, по которым будет добавляться новая запись в админке.
    exclude = ['slug']  # Исключает поле slug при создании
    # readonly_fields = ['year'] # запрещает редактировать это поле при создании
    ordering = ['-rating', 'name']  # Сортировка
    list_per_page = 10  # Количество элементов, отображаемых на странице.
    actions = ['set_dollars', 'set_euro', 'set_rubles']
    search_fields = ['name', ]        # Поля по которым будет осуществляться поиск
    list_filter = [RatingFilter]      # фильтр по следующим полям.
    filter_horizontal = ['actors']    # Для отображения поля Актёров в редактировании при связи many to many

    @admin.display(ordering='rating',
                   description='рекомендации')  # ДЛЯ ВОЗМОЖНОСТИ СОРТИРОВКИ В АДМИН ПАНЕЛИ. descr= ДЛЯ ОТОБРАЖЕНИЯ НАЗВ. КОЛОНКИ
    def rating_description(self, movie: Movie):
        if movie.rating < 68:
            return "Не рекомендовано к просмотру."
        if movie.rating < 80:
            return "Можно посмотреть! Не пожалеете!"
        return "Обязательно к просмотру!"

    @admin.action(description='Установить валюту DOLLAR')  # Описание в админке
    def set_dollars(self, request, qs: QuerySet):
        """Создаю функцию(ии), которая позволяет производить действие (action) в админке"""
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
            f'Было обновлено {count_updated}'
        )

    @admin.action(description='Установить валюту RUBLES')  # Описание в админке
    def set_rubles(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.RUB)
        self.message_user(
            request,
            f'Было обновлено {count_updated} записей'
        )


admin.site.register((Actor, Director, DressingRoom))      # Можно регать, передавая аргументы через кортеж

