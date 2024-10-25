import secrets

from django.core.mail import send_mail

from rest_framework import viewsets, status, generics
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from lms.permissions import IsOwner

from config.settings import EMAIL_HOST_USER
from users.models import PayMent, User
from users.api.stripe_utils import (
    create_price, create_product,
    create_checkout_session, get_session_status
)
from users.api.serializers import (
    MyTokenObtainPairSerializer, PayMentSerializer,
    MyTokenRefreshSerializer, UserSerializer
)


# ------------------------------------------------------ юзеры ------------------------------------------------------
class UserCreateView(generics.CreateAPIView):
    """Создание нового юзера"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.set_password(user.password)
        token_auf = secrets.token_hex(16)  # генерит токен
        user.token_auf = token_auf
        user.save()
        host = self.request.get_host()  # это получение хоста
        url = f'http://{host}/verify/{token_auf}'
        send_mail(
            subject=f'Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().perform_create(serializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для просмотра, редактирования и деактивации пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner | IsAdminUser]

    def get_queryset(self):
        """
        Возвращает список пользователей в зависимости от прав доступа.
        """
        if self.request.user.has_perm('users.is_admin'):
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST', detail='Создание профиля через этот эндпоинт запрещено.')

    def destroy(self, request, *args, **kwargs):
        """
        Деактивирует пользователя вместо его удаления.
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'Профиль удален'}, status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    permission_classes = [AllowAny]


#  ------------------------------------------------------ оплата ------------------------------------------------------
class PayMentViewSet(viewsets.ModelViewSet):
    """Для оплаты"""
    queryset = PayMent.objects.all()
    serializer_class = PayMentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    http_method_names = ['get', 'post']

    # Фильтрация
    search_fields = ['course__title', 'lesson__title', 'method_payment']
    ordering_fields = ['data_payment']
    ordering = ['data_payment']  # по умолчанию

    def get_queryset(self):
        """Пользователи видят только свои оплаты"""
        return PayMent.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'], url_path='stripe')
    def get_payment_status(self, request, pk=None):
        """
        Получить статус сессии платежа из Stripe.
        """
        payment_instance = self.get_object()

        if not payment_instance.payment_id:
            return Response({"error": "Нет ID платежа для этой записи."}, status=status.HTTP_400_BAD_REQUEST)
        session_status = get_session_status(payment_instance.payment_id)

        if "error" in session_status:
            return Response({"error": session_status["error"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(session_status, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='stripe')
    def create_payment(self, request):
        """
        Обработка создания платежа.
        """
        request.data['method_payment'] = 'C'
        serializer = PayMentSerializer(data=request.data)
        if serializer.is_valid():
            payment_instance = serializer.save(user=request.user)  # Привязка платежа к текущему пользователю
            course = payment_instance.course.first()
            lesson = payment_instance.lesson.first()

            # Создание продукта и цены в Stripe
            product_name = course.title if course else lesson.title
            amount_in_cents = int(payment_instance.sum_payment * 100)  # сумма в копейках!!!!
            product = create_product(product_name)  # продукт
            price = create_price(product['id'], amount_in_cents)  # цена
            session = create_checkout_session(price['id'])  # сессия

            # Сохранение ID платежа Stripe и ссылки на оплату
            payment_instance.payment_id = session['id']
            payment_instance.status_payment = PayMent.StatusPay.NOT_PAID
            payment_instance.save()

            return Response({
                "session_url": session['url'],
                "payment_id": payment_instance.id,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
