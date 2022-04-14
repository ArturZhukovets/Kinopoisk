"""Записи в таблицу БД можно осуществлять с помощью python manage.py shell или manage.py shell_plus --print-sql
Если пользоваться django-extensions - нужно установить её в терминале pip install и засунуть в INSTALLED_APS
Запрос на добавление записи в БД через shell питона осуществляется:
---НАЗВАНИЕ КЛАССА(ИМЯ_СТОЛБЦА='ЗНАЧЕНИЕ').save()---
Также для подсвечивания синтаксиса и подсказок установил в вирт. окружение пакет ipython запускается он в терминале командой ipython

Помимо записей в БД через python shell_plus / python shell очевидно можно записывать через сам SQL запрос.

Получать записи из таблицы (SELECT) можно делать из shell_plus:
---НАЗВАНИЕ_КЛАССА.objects.all()--- на выходе получаем сет из объектов. Можно делать запрос по индексу или по срезу

Изменять БД можно через БД запросы, а можно через shell, для изменения через shell необходимо создать объект класса в
котором будет содержаться колонка с контентом из БД:
---ИМЯ_ОБЪЕКТА = НАЗВАНИЕ_КЛАССА.objects.all()[ИНДЕКС]---
---ИМЯ_ОБЪЕКТА.ИМЯ_СТОЛБЦА = НОВОЕ_ЗНАЧЕНИЕ---
---ИМЯ_ОБЪЕКТА.save()      для удаления: ---ИМЯ_ОБЪЕКТА.delete()---

!!!!!!!!!!  ДОКУМЕНТАЦИЯ ПО РАБОТЕ С QUERYSET https://docs.djangoproject.com/en/3.2/ref/models/querysets/
Фильтрация. Метод get() позволяет получить любую ОДНУ запись с уникальным значением столбца (проще всего исп. с id)
            Метод filter() может возвращать несколько записей рабоатет как WHERE в SQL (objects.filter(year__isnull=False)) (objects.filter(year__isnull=True, name='Avatar'))
__contains - СОДЕРЖИТ, __startswith - НАЧИНАЕТСЯ С, __endswith - ЗАКАНЧИВАЕТСЯ, __in - аналог python IN, __gt - БОЛЬШЕ ЧЕМ, __lt - МЕНЬШЕ ЧЕМ
            Метод create() позволяет создавать объект без метода save(). ---Movie.objects.create(name='Avatar-2', rating=83)---
            Метод exclude() работает как filter, но он ИСКЛЮЧАЕТ из выборки (как !=)

Метод Q. from django.db import Q. Для работы с объектом Q, Q ставится перед условием и условие оборачивается в скобки.
---Movie.objects.filter(Q(year__isnull=True)), Q(rating=80)---
Q может содержать условия AND и OR. AND = &, OR = |, также можно использовать NOT, в этом случае NOT = '~'
---Movie.objects.filter(Q(year__isnull=True) |  Q(rating=80))---
также можно использовать NOT, в этом случае NOT = '~'
---Movie.objects.filter(~Q(year__isnull=True))--- выборка из year НЕ null


            """


from django.db import models

# from movie_app.models import Movie



class Movie(models.Model):
    """Создаю таблицу, через ООП. Создаётся класс, он будет являться таблицей. Наследуется от models.Model.
     Дальше в качестве атрибутов этого класса создаются колонки. Колонка ID создаётся автоматически ID_PRIMARY_KEY auto_increment
     После создания модели, в БД ничего отображаться не будет, до того как я не подтвержу Миграции (manage.py makemigrations
     manage.py migrations)."""
    name = models.CharField(max_length=40)              # создаю поле, в котором содержится строка не более 40 символов
    rating = models.IntegerField()                      # создаю поле, в котором содержатся только числа integer
    year = models.IntegerField(null=True)               # позволил сохранять в таблице значение Null
    budget = models.IntegerField(default=1000000)                      # установил дефолтное значение

    def __str__(self):                                  # методом __str__ можно поменять тип отображения объектов.
        return f'{self.name} - {self.rating}%'          # метод стр переопределяет поведение экземпляров


#  python manage.py shell_plus --print-sql
