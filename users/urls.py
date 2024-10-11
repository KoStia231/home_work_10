from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    UserLoginView, UserRegisterView, UserProfileUpdateView,
    UserProfileView, verify_mail, reset_password, index
)

app_name = UsersConfig.name

urlpatterns = [
                  path('', index, name='index'),
                  path('login/', UserLoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', UserRegisterView.as_view(), name='register'),

                  path('profile-update/<int:pk>', UserProfileUpdateView.as_view(), name='profile_update'),
                  path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),

                  path('verify/<str:token_auf>', verify_mail, name='verify'),
                  path('reset_password/', reset_password, name='reset_password'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
