from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet, LessonViewSet
)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'lessons', LessonViewSet)  # ----- уроки -----
router.register(r'courses', CourseViewSet)  # ----- курсы -----

urlpatterns = [
                  path('', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
