from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from lms.task import send_course_update_email

from lms.models import (
    Lesson, Course,
    Subscription
)
from lms.paginators import MyPageNumberPagination
from lms.permissions import (
    IsOwner, IsModer
)
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
    pagination_class = MyPageNumberPagination

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
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModer)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, IsOwner)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        """
        При обновлении курса отправляет письма подписчикам.
        """
        response = super().update(request, *args, **kwargs)
        course = self.get_object()
        subscriptions = Subscription.objects.filter(course=course)
        subscriber_emails = [subscription.user.email for subscription in subscriptions]
        for email in subscriber_emails:
            send_course_update_email.delay(email, course.title)

        return response


# ------------------------------------------------------ уроки ------------------------------------------------------
class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для уроков.
    Модератор может просматривать и редактировать все уроки.
    Пользователь может просматривать, редактировать и удалять только свои уроки.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPageNumberPagination

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
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModer)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, IsOwner)
        return super().get_permissions()


# ----------------------------------------------------- подписка -----------------------------------------------------
class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            message = 'Подписка уже есть'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = self.request.user
        subscriptions = Subscription.objects.filter(user=user)
        if subscriptions.exists():
            subscribed_courses = [subscription.course.title for subscription in subscriptions]
            return Response({"subscribed_courses": subscribed_courses})
        return Response({"message": "Нет подписок"})

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписки не обнаружено'

        return Response({"message": message})

