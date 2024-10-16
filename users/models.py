from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


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

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('manager', 'Может блокировать пользователей сервиса'),
            ('moderator', 'Может просматривать и редактировать любые уроки и курсы'),
        ]

    def __str__(self):
        return f'{self.first_name},{self.email}, {self.phone_number}, {self.get_group_permissions()} '


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
