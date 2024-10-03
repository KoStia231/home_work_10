from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Lesson, Course
from users.models import PayMent


class PayMentSerializer(ModelSerializer):
    class Meta:
        model = PayMent
        fields = '__all__'

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ('lesson_count', 'lessons')

    def get_lesson_count(self, obj):
        return obj.lessons.count()
