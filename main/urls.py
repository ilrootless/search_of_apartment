from django.urls import path

from .views import *

app_name = 'main'
urlpatterns = [
    # Парсинг авито
    path('result_avito/', result_avito, name='result_avito'),
    # Парсинг ЦИАН
    path('result_cian/', result_cian, name='result_cian'),
    # Активация польлзователя
    path('accounts/register/activate/<str:sign>', user_activate, name='register_activate'),
    # Завершение регистрации
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    # Регистрация и отправка письма
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    # вход
    path('accounts/login/', SOALoginView.as_view(), name='login'),
    # Выход
    path('accounts/logout/', SOALogoutView.as_view(), name='logout'),
    # Сохранение шаблона
    path('accounts/profile/template/save/', template_save, name='template_save'),
    # Поиск по сохраненному шаблону
    path('accounts/profile/template/search/<int:pk>/', template_search, name='template_search'),
    # Удаление шаблона поиска
    path('accounts/profile/template/delete/<int:pk>/', template_delete, name='template_delete'),
    # Сохранение объявления в избранное
    path('accounts/profile/favorite/save/', favorite_save, name='favorite_save'),
    # Удаление объявления из избранного
    path('accounts/profile/favorite/delete/<int:pk>', favorite_delete, name='favorite_delete'),
    # Правка личных данных
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    # Удаление зарегистирированного пользователя
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    # Профиль пользователя
    path('accounts/profile/', profile, name='profile'),
    # Прака пароля пользователя
    path('accounts/password/change/', SOAPasswordChangeView.as_view(), name='password_change'),
    # Сброс пароля и задание нового
    path('accounts/password/reset/<uidb64>/<token>', SOAPasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    # Вывод формы и оправка письма сброса пароля    
    path('accounts/password/reset/', SOAPasswordResetView.as_view(), name='password_reset'), 
    # Справка
    path('help/<str:page>/', help, name='help'),
    path('', index, name='index'),        
]

