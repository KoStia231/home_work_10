import random
import secrets
import string

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from config.settings import EMAIL_HOST_USER
from users.forms import UserLoginForm
from users.forms import UserRegisterForm, UserProfileUpdateForm, UserProfileUpdateFormManager
from users.models import User


class MyLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для всех страниц, которые требуют авторизации"""
    login_url = 'users:login'
    redirect_field_name = "redirect_to"


class UserLoginView(LoginView):
    """Страничка входа"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True  # авторизовать пользователя при успешном входе


def index(request):
    """Страничка главной страницы"""
    if request.user.is_authenticated:  # переход в профиль если авторизован
        return redirect(reverse('users:profile', kwargs={'pk': request.user.pk}))
    else:  # на регистрацию если не авторизован
        return redirect('users:login')


class UserRegisterView(CreateView):
    """Страничка регистрации нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/registr.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка пользователю письма с подтверждением регистрации"""
        user = form.save()
        user.is_active = False
        token_auf = secrets.token_hex(16)  # генерит токен
        user.token_auf = token_auf
        user.save()
        host = self.request.get_host()  # это получение хоста
        url = f'http://{host}/verify/{token_auf}'
        send_mail(
            subject=f'Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def verify_mail(request, token_auf):
    """Подтверждение регистрации переход по ссылке из письма и редирект на страницу входа"""
    user = get_object_or_404(User, token_auf=token_auf)  # получить пользователя по токен
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    """Сброс пароля и отправка письма """

    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            # это чтобы яндекс не пытался отправить письмо на не существующий адрес
            return render(request, template_name='users/reset_password.html')
        else:
            user = get_object_or_404(User, email=email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # генерит новый пароль
            user.set_password(new_password)
            user.save()
            send_mail(
                subject=f'Сброс пароля',
                message=f'Ваш новый пароль: {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )
        return redirect(reverse('users:login'))

    return render(request, template_name='users/reset_password.html')


class UserProfileUpdateView(MyLoginRequiredMixin, UpdateView):
    """Страничка редактирования профиля пользователя"""
    model = User
    success_url = reverse_lazy('users:profile')

    def get_success_url(self):
        return reverse('users:profile', args=[self.object.pk])

    def form_valid(self, form):
        """Сохранение измененных данных пользователя"""
        user = form.save(commit=False)
        password = self.request.POST.get('new_password')  # получить пароль из POST запроса
        if password != '':  # если поле пароля не пустое, заменить
            user.set_password(password)  # заменить пароль на новый пароль
            user.new_password = None  # очистить поле нового пароля
        user.save()  # сохранить изменения
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object:
            return UserProfileUpdateForm
        if user.has_perm('users.manager'):
            return UserProfileUpdateFormManager


class UserProfileView(MyLoginRequiredMixin, DetailView):
    """Страничка просмотра профиля пользователя"""
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        """контекст"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_'] = user
        context['token_access'] = AccessToken.for_user(user) if user.is_authenticated else None
        context['token_refresh'] = RefreshToken.for_user(user) if user.is_authenticated else None
        return context
