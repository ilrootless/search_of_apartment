from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin 
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .utilities import signer
from .parsers.avito import parsing_avito
from .parsers.cian import parsing_cian


# Главная страница
def index(request):
    context = {'form': UserSearchForm, 'captcha': CaptchaForm}
    return render(request, 'main/index.html', context)

# Парсинг авито
def result_avito(request):
    if request.method == 'POST':
        if not request.user.is_authenticated and 'captcha' not in request.session:
            post_params = UserSearchForm(request.POST)
            post_captcha = CaptchaForm(request.POST)
            valid = post_params.is_valid() and post_captcha.is_valid()
        else:
            post_params = UserSearchForm(request.POST)
            post_captcha = CaptchaForm
            valid = post_params.is_valid()
        if valid:
            request.session['captcha'] = 1
            global P, ADS
            P = post_params
            ADS = parsing_avito(post_params.cleaned_data)
            paginator = Paginator(ADS, 10)
            page = paginator.get_page(1)
            context = {'form': P, 'captcha': CaptchaForm, 'name': SearchNameForm, 'ads': page.object_list, 'page': page}
            return render(request, 'main/result_avito.html', context)
        else:
            context = {'form': post_params, 'captcha': post_captcha}
            return render(request, 'main/index.html', context)
    else:
        paginator = Paginator(ADS, 10)

        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'form': P, 'captcha': CaptchaForm, 'name': SearchNameForm, 'ads': page.object_list, 'page': page}
        return render(request, 'main/result_avito.html', context)


# Парсинг ЦИАН
def result_cian(request):
    if request.method == 'POST':
        if not request.user.is_authenticated and 'captcha' not in request.session:
            post_params = UserSearchForm(request.POST)
            post_captcha = CaptchaForm(request.POST)
            valid = post_params.is_valid() and post_captcha.is_valid()
        else:
            post_params = UserSearchForm(request.POST)
            post_captcha = CaptchaForm
            valid = post_params.is_valid()
        if valid:
            request.session['captcha'] = 1
            global P, ADS
            P = post_params
            ADS = parsing_cian(post_params.cleaned_data)
            paginator = Paginator(ADS, 10)
            page = paginator.get_page(1)
            context = {'form': P, 'captcha': CaptchaForm, 'name': SearchNameForm, 'ads': page.object_list, 'page': page}
            return render(request, 'main/result_cian.html', context)
        else:
            context = {'form': post_params, 'captcha': post_captcha}
            return render(request, 'main/index.html', context)
    else:
        paginator = Paginator(ADS, 10)

        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'form': P, 'captcha': CaptchaForm, 'name': SearchNameForm, 'ads': page.object_list, 'page': page}
        return render(request, 'main/result_cian.html', context)

# Сохранение шаблона поиска
@login_required
def template_save(request):
    post = UserSearchForm(request.POST)
    if post.is_valid():
        s = ST()
        s.advuser = request.user
        if 'rental' in post.cleaned_data['type_of_transaction']:
            s.rental = True
        if 'purchase' in post.cleaned_data['type_of_transaction']:
            s.purchase = True
        if 'new_building' in post.cleaned_data['novelty']:
            s.new_building = True
        if 'secondary' in post.cleaned_data['novelty']:
            s.secondary = True
        if 0 in post.cleaned_data['number_of_rooms']:
            s.studio = True
        if 1 in post.cleaned_data['number_of_rooms']:
            s.NOF_1 = True
        if 2 in post.cleaned_data['number_of_rooms']:
            s.NOF_2 = True
        if 3 in post.cleaned_data['number_of_rooms']:
            s.NOF_3 = True
        if 4 in post.cleaned_data['number_of_rooms']:
            s.NOF_4 = True
        if 5 in post.cleaned_data['number_of_rooms']:
            s.NOF_5 = True
        if 6 in post.cleaned_data['number_of_rooms']:
            s.NOF_gte_6 = True
        s.price_from = post.cleaned_data['price_from']
        s.price_up_to = post.cleaned_data['price_up_to']
        if 'Admiralteyskiy' in post.cleaned_data['district']:
            s.Admiralteyskiy = True
        if 'Vasileostrovskiy' in post.cleaned_data['district']:
            s.Vasileostrovskiy = True
        if 'Vyborgskiy' in post.cleaned_data['district']:
            s.Vyborgskiy = True
        if 'Kalininskiy' in post.cleaned_data['district']:
            s.Kalininskiy = True
        if 'Kirovsky' in post.cleaned_data['district']:
            s.Kirovsky = True
        if 'Kolpinsky' in post.cleaned_data['district']:
            s.Kolpinsky = True
        if 'Krasnogvardeisky' in post.cleaned_data['district']:
            s.Krasnogvardeisky = True
        if 'Krasnoselsky' in post.cleaned_data['district']:
            s.Krasnoselsky = True
        if 'Kronshtadtskiy' in post.cleaned_data['district']:
            s.Kronshtadtskiy = True
        if 'Kurortnyy' in post.cleaned_data['district']:
            s.Kurortnyy = True
        if 'Moskovskiy' in post.cleaned_data['district']:
            s.Moskovskiy = True
        if 'Nevsky' in post.cleaned_data['district']:
            s.Nevsky = True
        if 'Petrogradsky' in post.cleaned_data['district']:
            s.Petrogradsky = True
        if 'Petrodvortsovyy' in post.cleaned_data['district']:
            s.Petrodvortsovyy = True
        if 'Primorskiy' in post.cleaned_data['district']:
            s.Primorskiy = True
        if 'Pushkinskiy' in post.cleaned_data['district']:
            s.Pushkinskiy = True
        if 'Frunzenskiy' in post.cleaned_data['district']:
            s.Frunzenskiy = True
        if 'Tsentralnyy' in post.cleaned_data['district']:
            s.Tsentralnyy = True
        if request.POST['name']:
            s.name = request.POST['name']
        else:
            s.name = 'Шаблон без названия'
        s.save()
        messages.add_message(request, messages.SUCCESS, 'Шаблон сохранен')
        return redirect('main:profile')
    else:
        context = {'form': post}
        return render(request, 'main/index.html', context)

# Применение шаблона поиска
@login_required
def template_search(request, pk):
    st = get_object_or_404(ST, pk=pk)
    initial = {}
    if st.rental:
        initial['type_of_transaction'] = ['rental',]
    if st.purchase:
        initial['type_of_transaction'] += ['purchase',]
    if st.new_building:
        initial['novelty'] = ['new_building',]
    if st.secondary:
        initial['novelty'] += ['secondary',]
    if st.studio:
        initial['number_of_rooms'] = [0,]
    if st.NOF_1:
        initial['number_of_rooms'] += [1,]
    if st.NOF_2:
        initial['number_of_rooms'] += [2,]
    if st.NOF_3:
        initial['number_of_rooms'] += [3,]
    if st.NOF_4:
        initial['number_of_rooms'] += [4,]
    if st.NOF_5:
        initial['number_of_rooms'] += [5,]
    if st.NOF_gte_6:
        initial['number_of_rooms'] += [6,]
    if st.price_from:
        initial['price_from'] = st.price_from
    if st.price_up_to:
        initial['price_up_to'] = st.price_up_to
    if st.Admiralteyskiy:
        initial['district'] = ['Admiralteyskiy',]
    if st.Vasileostrovskiy:
        initial['district'] += ['Vasileostrovskiy',]
    if st.Vyborgskiy:
        initial['district'] += ['Vyborgskiy',]
    if st.Kalininskiy:
        initial['district'] += ['Kalininskiy',]
    if st.Kirovsky:
        initial['district'] += ['Kirovsky',]
    if st.Kolpinsky:
        initial['district'] += ['Kolpinsky',]
    if st.Krasnogvardeisky:
        initial['district'] += ['Krasnogvardeisky',]
    if st.Krasnoselsky:
        initial['district'] += ['Krasnoselsky',]
    if st.Kronshtadtskiy:
        initial['district'] += ['Kronshtadtskiy',]
    if st.Kurortnyy:
        initial['district'] += ['Kurortnyy',]
    if st.Moskovskiy:
        initial['district'] += ['Moskovskiy',]
    if st.Nevsky:
        initial['district'] += ['Nevsky',]
    if st.Petrogradsky:
        initial['district'] += ['Petrogradsky',]
    if st.Petrodvortsovyy:
        initial['district'] += ['Petrodvortsovyy',]
    if st.Primorskiy: 
        initial['district'] += ['Primorskiy',]
    if st.Pushkinskiy: 
        initial['district'] += ['Pushkinskiy',]
    if st.Frunzenskiy: 
        initial['district'] += ['Frunzenskiy',]
    if st.Tsentralnyy: 
        initial['district'] += ['Tsentralnyy',]

    form = UserSearchForm(initial=initial)
    context = {'form':form}
    return render(request, 'main/index.html', context)

# Удаление шаблона поиска
@login_required
def template_delete(request, pk):
    st = get_object_or_404(ST, pk=pk)
    messages.add_message(request, messages.SUCCESS, 'Шаблон "' + st.name + '" удален')
    st.delete()
    return redirect('main:profile')

# Сохранение объявления в избранное
@login_required
def favorite_save(request):
    f = FA()
    f.advuser = request.user
    f.title = request.POST['title']
    f.link = request.POST['link']
    f.image = request.POST['image']
    f.price = request.POST['price']
    f.address = request.POST['address']
    f.date = request.POST['date']
    f.agency = request.POST['agency']
    f.save()
    #messages.add_message(request, messages.SUCCESS, f'Объявление "{f.title}" сохранено')
    messages.add_message(request, messages.SUCCESS, 'Объявление "{0}" сохранено'.format(f.title))
    return redirect('main:profile')

# Удаление объявления из избранного
@login_required
def favorite_delete(request, pk):
    fa = get_object_or_404(FA, pk=pk)
    #messages.add_message(request, messages.SUCCESS, f'Объявление "{fa.title}" удалено из избранного.')
    messages.add_message(request, messages.SUCCESS, 'Объявление "{0}" удалено из избранного.'.format(fa.title))
    fa.delete()
    return redirect('main:profile')

# Регистрация и отправка письма активации
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

# Вывод сообщения об успешной регистрации
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

# Активация нового пользователя. По ссылке из письма
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        # Если интерент адресс из письма скомпроментирован, открывается соответствующуя страница с предложение зарегистрироваться заново
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    # Если пользователь уже был активирован, то открывается соответствующая страница
    if user.is_activated:
        template = 'main/user_is_activated.html'
    # Если все хорошо, активируем нового пользователя
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

# Вход
class SOALoginView(LoginView):
    template_name = 'main/login.html'

# Выход
class SOALogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

# профиль пользователя
@login_required
def profile(request):
    sts = ST.objects.filter(advuser=request.user).order_by('-saved_at')
    fas = FA.objects.filter(advuser=request.user).order_by('-saved_at')
    context = {'sts': sts, 'fas': fas}
    return render(request, 'main/profile.html', context)

# Правка личных данных пользователем
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

# Правка пароля
class SOAPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

# Инициализация сброса пароля, отпавка письма
class SOAPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/password_reset.html'
    success_url = reverse_lazy('main:profile')
    #success_message = 'Письмо для сброса пароля отправленно на указанный адрес электронной почты'
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_email.txt'
    
    def post(self, request, *args, **kwargs):
        emails = []
        for user in AdvUser.objects.all():
            if user.is_active:
                emails.append(user.email)

        if request.POST['email'] in emails:
            messages.add_message(request, messages.SUCCESS, 'Письмо для сброса пароля отправленно на указанный адрес электронной почты')
        else:
            messages.add_message(request, messages.ERROR, 'Пользователь с таким адресом электронной почты не найден')
        return super().post(request, *args, **kwargs)

# Собственно сброс пароля
class SOAPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Новый пароль пользователя задан'

# Удаление зарегистрированного пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

# Справка
def help(request, page):
    try:
        template = get_template('main/help/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

