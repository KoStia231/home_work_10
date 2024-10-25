from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import ValidationError

from users.models import PayMent, User
from lms.models import Lesson, Course


#  ------------------------------------------------------ юзеры ------------------------------------------------------
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'avatar',
                  'country']

    def validate(self, attrs):
        """Проверка на изменения системных полей"""
        read_only_fields = ['id', 'last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions']

        for field in read_only_fields:
            if field in attrs:
                raise serializers.ValidationError(f"Изменение поля '{field}' запрещено.")

        return attrs


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


#  ------------------------------------------------------ оплата ------------------------------------------------------
class PayMentSerializer(ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all(), required=False)
    lesson = serializers.PrimaryKeyRelatedField(many=True, queryset=Lesson.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PayMent
        fields = '__all__'

    def validate(self, data):
        if not data.get('course') and not data.get('lesson'):
            raise ValidationError("Необходимо указать хотя бы один курс или урок.")
        return data

