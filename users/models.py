from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


# Кастомный менеджер пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с email и паролем.
        """
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    first_name = models.CharField(verbose_name='имя', max_length=30, unique=True)
    email = models.EmailField(verbose_name='почта', unique=True)
    phone_number = models.IntegerField(verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(verbose_name='аватарка', **NULLABLE)
    country = models.CharField(verbose_name='страна', max_length=100, **NULLABLE)

    new_password = models.CharField(verbose_name='Новый пароль', max_length=100, **NULLABLE)
    token_auf = models.CharField(max_length=255, **NULLABLE, verbose_name='Токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('manager', 'Может блокировать пользователей сервиса'),
            ('moderator', 'Может просматривать и редактировать любые уроки и курсы'),
        ]

    def __str__(self):
        return (f'Имя-{self.first_name}|Почта-{self.email}'
                f'|Телефон-{self.phone_number}|Модер-{self.has_perm('moderator')}, ')


class PayMent(models.Model):
    class MethodsPay(models.TextChoices):
        CASH = 'C', 'наличные'
        BANK_TRANSFER = 'B', 'перевод'

    class StatusPay(models.TextChoices):
        PAID = 'P', 'оплачен'
        NOT_PAID = 'N', 'не оплачен'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    data_payment = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    method_payment = models.CharField(max_length=1, choices=MethodsPay.choices, verbose_name='метод оплаты')
    sum_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    course = models.ManyToManyField(Course, verbose_name="Оплаченные курсы")
    lesson = models.ManyToManyField(Lesson, verbose_name="Оплаченные уроки")

    status_payment = models.CharField(
        max_length=1, choices=StatusPay.choices,
        default=StatusPay.NOT_PAID, verbose_name='статус оплаты'
    )

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'

    def __str__(self):
        return f'{self.user} - {self.get_status_payment_display()} - {self.data_payment}'
