from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from lms.models import Lesson, Course
from lms.permissions import IsOwner, IsModer
from lms.serializers import (
    LessonSerializer, CourseSerializer,
)


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
        Модераторам запрещено создавать и удалять уроки.
        Владельцы могут редактировать и удалять свои уроки.
        """
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModer)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, IsOwner)
        return super().get_permissions()


# ------------------------------------------------------ уроки ------------------------------------------------------
class LessonViewSet(CourseViewSet, viewsets.ModelViewSet):
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

