from rest_framework.serializers import ModelSerializer

from lms.models import Lesson, Course


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
