from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification

# Модель пользователя
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        pass

# Объявление сигнала регистрации пользователя и привязка к нему обрaботчика
user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)

# Модель шаблонов поиска
class ST(models.Model):
    advuser = models.ForeignKey(AdvUser, on_delete=models.CASCADE, db_index=True, verbose_name='Пользователь')
    name = models.CharField(max_length=100, blank=True, verbose_name='Имя шаблона')
    rental = models.BooleanField(default=False, db_index=True, verbose_name='Аренда')
    purchase = models.BooleanField(default=False, db_index=True, verbose_name='Покупка')
    new_building = models.BooleanField(default=False, db_index=True, verbose_name='Новостройка')
    secondary = models.BooleanField(default=False, db_index=True, verbose_name='Вторичка')
    studio = models.BooleanField(default=False, db_index=True, verbose_name='Студия')
    NOF_1 = models.BooleanField(default=False, db_index=True, verbose_name='1')
    NOF_2 = models.BooleanField(default=False, db_index=True, verbose_name='2')
    NOF_3 = models.BooleanField(default=False, db_index=True, verbose_name='3')
    NOF_4 = models.BooleanField(default=False, db_index=True, verbose_name='4')
    NOF_5 = models.BooleanField(default=False, db_index=True, verbose_name='5')
    NOF_gte_6 = models.BooleanField(default=False, db_index=True, verbose_name='6+')
    price_from = models.IntegerField(null=True, blank=True, db_index=True, verbose_name='Цена от (руб.)')
    price_up_to = models.IntegerField(null=True, blank=True, db_index=True, verbose_name='Цена до (руб.)')
    Admiralteyskiy = models.BooleanField(default=False, db_index=True, verbose_name='Адмиралтейский')
    Vasileostrovskiy = models.BooleanField(default=False, db_index=True, verbose_name='Василеостровский')
    Vyborgskiy = models.BooleanField(default=False, db_index=True, verbose_name='Выборгский')
    Kalininskiy = models.BooleanField(default=False, db_index=True, verbose_name='Калининский')
    Kirovsky = models.BooleanField(default=False, db_index=True, verbose_name='Кировский')
    Kolpinsky = models.BooleanField(default=False, db_index=True, verbose_name='Колпинский')
    Krasnogvardeisky = models.BooleanField(default=False, db_index=True, verbose_name='Красногвардейский')
    Krasnoselsky = models.BooleanField(default=False, db_index=True, verbose_name='Красносельский')
    Kronshtadtskiy = models.BooleanField(default=False, db_index=True, verbose_name='Кронштадтский')
    Kurortnyy = models.BooleanField(default=False, db_index=True, verbose_name='Курортный')
    Moskovskiy = models.BooleanField(default=False, db_index=True, verbose_name='Московский')
    Nevsky = models.BooleanField(default=False, db_index=True, verbose_name='Невский')
    Petrogradsky = models.BooleanField(default=False, db_index=True, verbose_name='Петроградский')
    Petrodvortsovyy = models.BooleanField(default=False, db_index=True, verbose_name='Петродворцовый')
    Primorskiy = models.BooleanField(default=False, db_index=True, verbose_name='Приморский')
    Pushkinskiy = models.BooleanField(default=False, db_index=True, verbose_name='Пушкинский')
    Frunzenskiy = models.BooleanField(default=False, db_index=True, verbose_name='Фрунзенский')
    Tsentralnyy = models.BooleanField(default=False, db_index=True, verbose_name='Центральный')
    saved_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата сохранения')

    class Meta:
        verbose_name = 'Шаблон поиска'
        verbose_name_plural = 'Шаблоны поиска'

    def __str__(self):
        return self.name

# Модель избранных объявлений
class FA(models.Model):
    advuser = models.ForeignKey(AdvUser, on_delete=models.CASCADE, db_index=True, verbose_name='Пользователь')
    title = models.CharField(max_length=100, verbose_name='Заголовок объявления')
    link = models.URLField(verbose_name='Избранное объявление')
    image = models.URLField(verbose_name='Изображение')
    price = models.CharField(max_length=50, verbose_name='Цена')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    date = models.CharField(max_length=50, verbose_name='Дата публикации объявления')
    agency = models.CharField(max_length=50, verbose_name='Агенство')
    saved_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата сохранения')

    class Meta:
        verbose_name = 'Избранное объявление'
        verbose_name_plural = 'Избранные объявления'

    def __str__(self):
        return self.title
