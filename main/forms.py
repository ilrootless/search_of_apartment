from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from captcha.fields import CaptchaField

from .models import *

# Форма изменения пароля пользователя
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name')

# Форма регистрации пользователя
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
        else:
            password1 = False
            #errors = {'password1': ValidationError('Пароль не отвечает всем требованиям', code='password_mismatch')}
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

# Форма поиска для авторизованного пользователя
class UserSearchForm(forms.Form):
    TOT_CHOICES = (
        ('rental', 'Аренда'),            
        ('purchase', 'Покупка'),            
    )
    type_of_transaction = forms.MultipleChoiceField(choices=TOT_CHOICES, required=False, widget=forms.widgets.CheckboxSelectMultiple, label='Вид сделки') 
    N_CHOICES = (
        ('new_building', 'Новостройка'),        
        ('secondary', 'Вторичка'),        
    )
    novelty = forms.MultipleChoiceField(choices=N_CHOICES, required=False, widget=forms.widgets.CheckboxSelectMultiple, label='Новизна квартиры')
    NOR_CHOICES = (
        ('0', 'Студия'),      
        ('1', '1'),      
        ('2', '2'),      
        ('3', '3'),      
        ('4', '4'),      
        ('5', '5'),      
        ('6', '6+'),      
    )
    number_of_rooms = forms.TypedMultipleChoiceField(choices=NOR_CHOICES, coerce=int, required=False, widget=forms.widgets.CheckboxSelectMultiple, label='Колличество комнат')
    price_from = forms.IntegerField(required=False, label='Цена от (в руб.)')
    price_up_to = forms.IntegerField(required=False, label='Цена до (в руб.)')
    D_CHOICES = (
        ('Admiralteyskiy', 'Адмиралтейский'),        
        ('Vasileostrovskiy', 'Василеостровский'),        
        ('Vyborgskiy', 'Выборгский'),        
        ('Kalininskiy', 'Калининский'),        
        ('Kirovsky', 'Кировский'),        
        ('Kolpinsky', 'Колпинский'),        
        ('Krasnogvardeisky', 'Красногвардейский'),        
        ('Krasnoselsky', 'Красносельский'),        
        ('Kronshtadtskiy', 'Кронштадтский'),        
        ('Kurortnyy', 'Курортный'),        
        ('Moskovskiy', 'Московский'),        
        ('Nevsky', 'Невский'),        
        ('Petrogradsky', 'Петроградский'),        
        ('Petrodvortsovyy', 'Петродворцовый'),        
        ('Primorskiy', 'Приморский'),        
        ('Pushkinskiy', 'Пушкинский'),        
        ('Frunzenskiy', 'Фрунзенский'),        
        ('Tsentralnyy', 'Центральный'),        
    )
    district = forms.MultipleChoiceField(choices=D_CHOICES, required=False, widget=forms.widgets.CheckboxSelectMultiple, label='Район')

    def clean(self):
        super().clean()
        errors = {}
        if self.cleaned_data['price_from']:
            if self.cleaned_data['price_from'] < 0:
                errors['price_from'] = ValidationError('Цена не может быть отрицательной')
        if self.cleaned_data['price_up_to']:
            if self.cleaned_data['price_up_to'] < 0:
                errors['price_up_to'] = ValidationError('Цена не может быть отрицательной')
        if self.cleaned_data['price_up_to'] and self.cleaned_data['price_from']:
            if self.cleaned_data['price_up_to'] < self.cleaned_data['price_from']:
             errors['price_up_to'] = ValidationError('Цена "до" не может быть меньше цены "от"')
        if errors:
            raise ValidationError(errors)

# Форма поиска для гостя
class CaptchaForm(forms.Form):
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})

# Форма названия шаблона
class SearchNameForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, label='Имя нового шаблона')
