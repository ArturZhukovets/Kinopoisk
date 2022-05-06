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
__contains - СОДЕРЖИТ, __startswith - НАЧИНАЕТСЯ С, __endswith - ЗАКАНЧИВАЕТСЯ, __in - аналог python IN, __gte - БОЛЬШЕ ЧЕМ, __lt - МЕНЬШЕ ЧЕМ
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
from django.urls import reverse
from django.utils.text import slugify    #Для slug
from django.utils.safestring import SafeText, mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator


class Director(models.Model):
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    director_email = models.EmailField(max_length=30)

    def __str__(self):
        return f'{self.second_name} {self.first_name}'


class Actor(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICEC = [
        ('m', 'MAN'),
        ('f', 'FEMALE'),

    ]
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    actor_gender = models.CharField(max_length=1, choices=GENDER_CHOICEC, default=MALE)

    def __str__(self):
        if self.actor_gender == self.MALE:
            return f'Актёр {self.first_name} {self.second_name}'
        elif self.actor_gender == self.FEMALE:
            return f'Актриса {self.first_name} {self.second_name}'


class Movie(models.Model):
    """Создаю таблицу, через ООП. Создаётся класс, он будет являться таблицей. Наследуется от models.Model.
     Дальше в качестве атрибутов этого класса создаются колонки. Колонка ID создаётся автоматически ID_PRIMARY_KEY auto_increment
     После создания модели, в БД ничего отображаться не будет, до того как я не подтвержу Миграции (manage.py makemigrations
     manage.py migrations)."""
    EURO = 'EUR'
    USD = 'USD'
    RUB = 'RUB'
    CURRENCY_CHOICES = [
        ('RUB', 'RUBLES'),
        ('EUR', 'EURO'),
        ('USD', 'DOLLARS')
    ]
    name = models.CharField(max_length=40)  # создаю поле, в котором содержится строка не более 40 символов
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])  # поле integer, в котором
    # Минимальное значение = 1, максимальное значение = 100
    year = models.IntegerField(null=True, blank=True)  # позволил сохранять в таблице значение Null, аргумент blank позволяет оставлять незаполненное поле
    budget = models.IntegerField(default=1000000, validators=[MinValueValidator(1)])  # установил дефолтное значение и мин. значение
    ### SlugField Специальный метод у класса models, позволяющий создавать Slug url
    slug = models.SlugField(max_length=30, default='', null=False, db_index=True, allow_unicode=True)  # По-дефолту пустая строка. allow_unicode для работы с кириллицей. db_index для более быстрого поиска
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=USD)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True)   # Один-ко-многим с таблицей Director
    actors = models.ManyToManyField(Actor)

    def save(self, *args, **kwargs):
        """Переопределяю метод save() у родительского класса Model"""
        self.slug = slugify(self.name, allow_unicode=True)       # Преобразовываю в слаг формат название фильма allow_unicod - для работы с кирилицей
        super(Movie, self).save(*args, **kwargs)

    def get_url(self):
        """Логику гиперссылки из шаблона html можно перенести в модель. Использую функцию reverse() в качестве аргумента айдишник объекта.
        В итоге в шаблоне я просто обращаюсь к классу Movie и обращаюсь к этой функции"""
        return reverse('movie_description', args=[self.slug, ])

    def __str__(self):  # методом __str__ можно поменять тип отображения объектов.
        return f'{self.name} - {self.rating}%'  # метод стр переопределяет поведение экземпляров

#  python manage.py shell_plus --print-sql
