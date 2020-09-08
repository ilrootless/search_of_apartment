from django.contrib import admin
import datetime

from .models import *
from .utilities import send_activation_notification

# Действие: отправка писем выбранным пользователям
def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с оповещениями отправлены')
send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации'

# Фильтр пользователей по прознаку активации
class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'activate'

    def lookups(self, request, model_admin):
        return (
                    ('activated', 'Прошли'),
                    ('threedays', 'Не прошли более 3 дней'),
                    ('week', 'Не прошли более недели'),
                )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)

# Редактор пользователей
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'), ('is_active', 'is_activated'), ('is_staff', 'is_superuser'), 'groups', 'user_permissions', ('last_login', 'date_joined'),)
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)

# Редактор шаблонов
class STAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'advuser', 'saved_at')
    search_fields = ('name',)
    date_hierarchy = 'saved_at'
    readonly_fields = ('saved_at',)
    fieldsets = (
        (None, {
            'fields': (('name', 'advuser'), 'saved_at'),
        }),        
        ('Виды сделки', {
            'fields': (('rental', 'purchase'),),
        }),
        ('Новизна квартиры', {
            'fields': (('new_building', 'secondary'),),
        }),
        ('Колличество комнат', {
            'fields': (('NOF_1', 'NOF_2', 'NOF_3', 'NOF_4', 'NOF_5', 'NOF_gte_6'),),
        }),
        ('Цена', {
            'fields': (('price_from', 'price_up_to'),),
        }),
        ('Районы', {
            'fields': (('Admiralteyskiy', 'Vasileostrovskiy', 'Vyborgskiy', 'Kalininskiy', 'Kirovsky', 'Kolpinsky', 'Krasnogvardeisky', 'Krasnoselsky', 'Kronshtadtskiy', 'Kurortnyy', 'Moskovskiy', 'Nevsky', 'Petrogradsky', 'Petrodvortsovyy', 'Primorskiy', 'Pushkinskiy', 'Frunzenskiy', 'Tsentralnyy'),),
        }),
    )

# Редактор избранных объявлений
class FAAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'advuser', 'agency', 'saved_at')
    search_fields = ('title', 'agency')
    date_hierarchy = 'saved_at'
    readonly_fields = ('title', 'link', 'image', 'price', 'address', 'date', 'agency', 'saved_at')

# Регистрация моделей и редакторов 
admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(ST, STAdmin)
admin.site.register(FA, FAAdmin)
