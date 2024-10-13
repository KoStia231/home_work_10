from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from lms.models import Lesson, Course
from users.models import PayMent, User


#  --------- юзеры ---------
class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['first_name'] = user.first_name
        token['email'] = user.email

        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    pass


#  --------- оплата ---------

class PayMentSerializer(ModelSerializer):
    class Meta:
        model = PayMent
        fields = '__all__'


#  --------- курсы и уроки ---------

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
