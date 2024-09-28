from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from lms.apps import LmsConfig

app_name = LmsConfig.name

urlpatterns = [
                  path('', ..., name='...'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
