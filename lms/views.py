import secrets

from django.core.mail import send_mail
from rest_framework import viewsets, status, generics
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.settings import EMAIL_HOST_USER
from lms.models import Lesson, Course
from lms.permissions import IsOwnerOrModerator, IsOwner
from lms.serializers import (
    MyTokenObtainPairSerializer, PayMentSerializer,
    LessonSerializer,
    CourseSerializer, MyTokenRefreshSerializer
)
from lms.serializers import UserSerializer
from users.models import PayMent
from users.models import User


# ------------------------------------------------------ юзеры ------------------------------------------------------
class UserCreateView(generics.CreateAPIView):
    """Создание нового юзера"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
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


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для создания, просмотра, редактирования и деактивации пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner | IsAdminUser]

    def get_queryset(self):
        """
        Возвращает список пользователей в зависимости от прав доступа.
        """
        if self.request.user.has_perm('users.is_admin'):  # Если пользователь администратор
            return User.objects.all()  # Возвращаем всех пользователей
        return User.objects.filter(id=self.request.user.id)  # Возвращаем только текущего пользователя

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST', detail='Создание профиля через этот эндпоинт запрещено.')

    def destroy(self, request, *args, **kwargs):
        """
        Деактивирует пользователя вместо его удаления.
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'Профиль удален'}, status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    permission_classes = [AllowAny]


#  ------------------------------------------------------ оплата ------------------------------------------------------
class PayMentViewSet(viewsets.ModelViewSet):
    """Для оплаты"""
    queryset = PayMent.objects.all()
    serializer_class = PayMentSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    # Фильтрация
    search_fields = ['course__title', 'lesson__title', 'method_payment']
    ordering_fields = ['data_payment']
    ordering = ['data_payment']  # по умолчанию


#  ------------------------------------------------------ курсы ------------------------------------------------------

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для курсов.
    Модератор может просматривать и редактировать все курсы.
    Пользователь может просматривать, редактировать и удалять только свои курсы.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Модераторы видят все курсы, а пользователи — только свои.
        """
        if self.request.user.has_perm('users.moderator'):
            return Course.objects.all()
        return Course.objects.filter(autor=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем права в зависимости от действия.
        Модераторам запрещено создавать и удалять курсы.
        Владельцы могут редактировать и удалять свои курсы.
        """
        if self.action in ['create', 'destroy']:
            if self.request.user.has_perm('users.moderator'):
                # Модераторам запрещено удалять и создавать курсы
                self.permission_classes = [IsAdminUser]  # Только администраторы могут создавать/удалять
            else:
                self.permission_classes = [IsOwner]  # Владелец может удалять свои курсы
        else:
            # Для всех остальных действий (редактирование, просмотр) применяем стандартные права
            self.permission_classes = [IsOwnerOrModerator | IsOwner]

        return super().get_permissions()


# ------------------------------------------------------ уроки ------------------------------------------------------
class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для уроков.
    Модератор может просматривать и редактировать все уроки.
    Пользователь может просматривать, редактировать и удалять только свои уроки.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Модераторы видят все уроки, а пользователи — только свои.
        """
        if self.request.user.has_perm('users.moderator'):
            return Lesson.objects.all()
        return Lesson.objects.filter(autor=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем права в зависимости от действия.
        Модераторам запрещено создавать и удалять уроки.
        Владельцы могут редактировать и удалять свои уроки.
        """
        if self.action in ['create', 'destroy']:
            if self.request.user.has_perm('users.moderator'):
                # Модераторам запрещено удалять и создавать уроки
                self.permission_classes = [IsAdminUser]  # Только администраторы могут создавать/удалять
            else:
                self.permission_classes = [IsOwner]  # Владелец может удалять свои уроки
        else:
            # Для всех остальных действий (редактирование, просмотр) применяем стандартные права
            self.permission_classes = [IsOwnerOrModerator | IsOwner]

        return super().get_permissions()
