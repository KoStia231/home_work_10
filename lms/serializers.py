from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Lesson, Course, Subscription
from lms.validators import YouTubeURLValidator


#  ------------------------------------------------------ уроки ------------------------------------------------------
class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YouTubeURLValidator(field='video_link')]


#  ------------------------------------------------------ курсы ------------------------------------------------------
class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ('lesson_count', 'lessons')

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()
