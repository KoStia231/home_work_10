from rest_framework import generics, viewsets

from .models import Lesson, Course
from .serializers import LessonSerializer, CourseSerializer





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
