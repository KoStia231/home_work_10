from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from celery import shared_task
from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_course_update_email(user_email, course_title):
    """Отправка письма пользователю о том, что курс обновлен."""
    send_mail(
        subject=f'Обновление курса: {course_title}',
        message=f'В курсе "{course_title}" появились новые материалы',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )


@shared_task
def deactivate_inactive_users():
    """
    Блок пользователей, которые не заходили более месяца, устанавливая is_active в False.
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
