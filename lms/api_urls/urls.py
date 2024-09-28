from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
                  path('', include(router.urls)),
                  path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
                  path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
