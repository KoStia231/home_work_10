from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.api.serializers import MyTokenObtainPairSerializer, PayMentSerializer
from users.models import PayMent


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PayMentViewSet(viewsets.ModelViewSet):
    """Для оплаты"""
    queryset = PayMent.objects.all()
    serializer_class = PayMentSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    # Фильтрация
    search_fields = ['course__title', 'lesson__title', 'method_payment']
    ordering_fields = ['data_payment']
    ordering = ['data_payment']  # по умолчанию
