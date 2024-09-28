from rest_framework.serializers import ModelSerializer

from lms.models import Lesson, Course


class CourseSerializer(ModelSerializer):
    """Класс сериализатора для модели Course"""

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    """Класс сериализатора для модели Lesson"""

    class Meta:
        model = Lesson
        fields = '__all__'
