from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet, LessonViewSet
)
from lms.views import (
    PayMentViewSet, UserCreateView,
    MyTokenObtainPairView, MyTokenRefreshView
)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'payments', PayMentViewSet)  # ----- оплата -----
router.register(r'lessons', LessonViewSet)  # ----- уроки -----
router.register(r'courses', CourseViewSet)  # ----- курсы -----

urlpatterns = [
                  path('', include(router.urls)),

                  # ----- юзеры -----
                  path('register/', UserCreateView.as_view(), name='register_api'),
                  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token-refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
