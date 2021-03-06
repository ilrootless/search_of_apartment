# Generated by Django 3.0.3 on 2020-04-12 14:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_activated', models.BooleanField(db_index=True, default=True, verbose_name='Прошел активацию?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ST',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Имя шаблона')),
                ('rental', models.BooleanField(db_index=True, default=False, verbose_name='Аренда')),
                ('purchase', models.BooleanField(db_index=True, default=False, verbose_name='Покупка')),
                ('new_building', models.BooleanField(db_index=True, default=False, verbose_name='Новостройка')),
                ('secondary', models.BooleanField(db_index=True, default=False, verbose_name='Вторичка')),
                ('studio', models.BooleanField(db_index=True, default=False, verbose_name='Студия')),
                ('NOF_1', models.BooleanField(db_index=True, default=False, verbose_name='1')),
                ('NOF_2', models.BooleanField(db_index=True, default=False, verbose_name='2')),
                ('NOF_3', models.BooleanField(db_index=True, default=False, verbose_name='3')),
                ('NOF_4', models.BooleanField(db_index=True, default=False, verbose_name='4')),
                ('NOF_5', models.BooleanField(db_index=True, default=False, verbose_name='5')),
                ('NOF_gte_6', models.BooleanField(db_index=True, default=False, verbose_name='6+')),
                ('price_from', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Цена от (руб.)')),
                ('price_up_to', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Цена до (руб.)')),
                ('Admiralteyskiy', models.BooleanField(db_index=True, default=False, verbose_name='Адмиралтейский')),
                ('Vasileostrovskiy', models.BooleanField(db_index=True, default=False, verbose_name='Василеостровский')),
                ('Vyborgskiy', models.BooleanField(db_index=True, default=False, verbose_name='Выборгский')),
                ('Kalininskiy', models.BooleanField(db_index=True, default=False, verbose_name='Калининский')),
                ('Kirovsky', models.BooleanField(db_index=True, default=False, verbose_name='Кировский')),
                ('Kolpinsky', models.BooleanField(db_index=True, default=False, verbose_name='Колпинский')),
                ('Krasnogvardeisky', models.BooleanField(db_index=True, default=False, verbose_name='Красногвардейский')),
                ('Krasnoselsky', models.BooleanField(db_index=True, default=False, verbose_name='Красносельский')),
                ('Kronshtadtskiy', models.BooleanField(db_index=True, default=False, verbose_name='Кронштадтский')),
                ('Kurortnyy', models.BooleanField(db_index=True, default=False, verbose_name='Курортный')),
                ('Moskovskiy', models.BooleanField(db_index=True, default=False, verbose_name='Московский')),
                ('Nevsky', models.BooleanField(db_index=True, default=False, verbose_name='Невский')),
                ('Petrogradsky', models.BooleanField(db_index=True, default=False, verbose_name='Петроградский')),
                ('Petrodvortsovyy', models.BooleanField(db_index=True, default=False, verbose_name='Петродворцовый')),
                ('Primorskiy', models.BooleanField(db_index=True, default=False, verbose_name='Приморский')),
                ('Pushkinskiy', models.BooleanField(db_index=True, default=False, verbose_name='Пушкинский')),
                ('Frunzenskiy', models.BooleanField(db_index=True, default=False, verbose_name='Фрунзенский')),
                ('Tsentralnyy', models.BooleanField(db_index=True, default=False, verbose_name='Центральный')),
                ('saved_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата сохранения')),
                ('advuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Шаблон поиска',
                'verbose_name_plural': 'Шаблоны поиска',
            },
        ),
        migrations.CreateModel(
            name='FA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок объявления')),
                ('link', models.URLField(verbose_name='Избранное объявление')),
                ('image', models.URLField(verbose_name='Изображение')),
                ('price', models.CharField(max_length=50, verbose_name='Цена')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('date', models.CharField(max_length=50, verbose_name='Дата публикации объявления')),
                ('agency', models.CharField(max_length=50, verbose_name='Агенство')),
                ('saved_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата сохранения')),
                ('advuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное объявление',
                'verbose_name_plural': 'Избранные объявления',
            },
        ),
    ]
