from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from lms.serializers import PayMentSerializer
from users.models import PayMent
from .models import Lesson, Course
from .serializers import LessonSerializer, CourseSerializer


class PayMentViewSet(viewsets.ModelViewSet):
    """Для оплаты"""
    queryset = PayMent.objects.all()
    serializer_class = PayMentSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    # Фильтрация
    search_fields = ['course__title', 'lesson__title', 'method_payment']
    ordering_fields = ['data_payment']
    ordering = ['data_payment']  # по умолчанию


class CourseViewSet(viewsets.ModelViewSet):
    """Для курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """Получение списка уроков и создание нового урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    """Получение списка уроков и создание нового урока"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление конкретного урока по его ID"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
