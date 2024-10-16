from users.apps import UsersConfig
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from users.api.views import (
    PayMentViewSet, UserCreateView, UserViewSet,
    MyTokenObtainPairView, MyTokenRefreshView
)


app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', PayMentViewSet)  # ----- оплата -----
router.register(r'profile', UserViewSet)  # ----- профиль -----

urlpatterns = [
                  path('', include(router.urls)),

                  # ----- регистрация и токен -----
                  path('register/', UserCreateView.as_view(), name='register_api'),
                  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token-refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
