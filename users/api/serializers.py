from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import PayMent


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['first_name'] = user.first_name
        token['email'] = user.email

        return token


class PayMentSerializer(ModelSerializer):
    class Meta:
        model = PayMent
        fields = '__all__'
