import os
from datetime import timedelta
from pathlib import Path
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG', False).lower() == 'true'

ALLOWED_HOSTS = list(os.getenv('DJANGO_ALLOWED_HOSTS'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# ----------------------------------------------- Application definition -----------------------------------------------
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',

    'users',
    'lms',
]

# ----------------------------------------------------- MIDDLEWARE -----------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------- TEMPLATES ------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------ Настройки JWT-токенов -----------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# ------------------------------------------ Настройки срока действия токенов ------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# ---------------------------------------------- AUTH_PASSWORD_VALIDATORS ----------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ---------------------------------------------- База данных PostgreSQL -----------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
    }
}

# -------------------------------------------------- Сервер для кеша ---------------------------------------------------
CACHES_ENABLED = os.getenv('DJANGO_CACHES_ENABLED', False).lower() == 'true'
if CACHES_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv('REDIS_LOCATION'),
        }
    }

# -------------------------------------------- Настройки для аутентификации --------------------------------------------
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------------- Настройки для почтового сервиса яндекса ---------------------------------------
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Почта
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Пароль приложения отправки
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False).lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', False).lower() == 'true'

# -------------------------------------------------- Настройки Stripe --------------------------------------------------
STRIPE_PUBLISHABLE_KEY = os.getenv('API_STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.getenv('API_STRIPE_SECRET_KEY')

# -------------------------------------------- Настройки почтового сервера ---------------------------------------------
EMAIL_CONSOLE = os.getenv('EMAIL_CONSOLE', False).lower() == 'true'
if EMAIL_CONSOLE:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ------------------------------------------------ Настройки для Celery ------------------------------------------------
# URL-адрес брокера сообщений
CELERY_BROKER_URL = os.getenv('REDIS_LOCATION')  # Например, Redis, который по умолчанию работает на порту 6379
CELERY_RESULT_BACKEND = os.getenv('REDIS_LOCATION')  # URL-адрес брокера результатов, также Redis
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = os.getenv('CELERY_TASK_TRACK_STARTED', False).lower() == 'true'
CELERY_TASK_TIME_LIMIT = 30 * 60  # Максимальное время на выполнение задачи

CELERY_BEAT_SCHEDULE = {
    'deactivate_inactive_users_daily': {
        'task': 'lms.tasks.deactivate_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # Запуск каждый день в полночь
    },
}
