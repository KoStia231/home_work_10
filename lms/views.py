import secrets

from django.core.mail import send_mail
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.settings import EMAIL_HOST_USER
from lms.models import Lesson, Course
from lms.permissions import IsOwnerOrModerator
from lms.serializers import (
    MyTokenObtainPairSerializer, PayMentSerializer,
    UserCreateSerializer, LessonSerializer,
    CourseSerializer, MyTokenRefreshSerializer
)
from users.models import PayMent, User


#  --------- юзеры ---------

class UserCreateView(generics.CreateAPIView):
    """Создание нового юзера"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.set_password(user.password)
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
        return super().perform_create(serializer)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    permission_classes = [AllowAny]


#  --------- оплата ---------
class PayMentViewSet(viewsets.ModelViewSet):
    """Для оплаты"""
    queryset = PayMent.objects.all()
    serializer_class = PayMentSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    # Фильтрация
    search_fields = ['course__title', 'lesson__title', 'method_payment']
    ordering_fields = ['data_payment']
    ordering = ['data_payment']  # по умолчанию


#  --------- курсы ---------

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для курсов.
    Модератор может просматривать и редактировать все курсы.
    Пользователь может просматривать, редактировать и удалять только свои курсы.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrModerator]

    def get_queryset(self):
        """
        Если пользователь не модератор, он видит только свои курсы.
        """
        if self.request.user.has_perm('users.moderator'):
            return Course.objects.all()
        return Course.objects.filter(author=self.request.user)


# --------- уроки ---------
class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для уроков.
    Модератор может просматривать и редактировать все уроки.
    Пользователь может просматривать, редактировать и удалять только свои уроки.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]

    def get_queryset(self):
        """
        Если пользователь не модератор, он видит только свои уроки.
        """
        if self.request.user.has_perm('users.moderator'):
            return Lesson.objects.all()
        return Lesson.objects.filter(author=self.request.user)

