"""
Django settings for subnet_project project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from celery import Celery
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9vq8ymi(d7njr)w_&zu3n769(o)76!tbnl+!*)^is14*rz95!*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'subnetPing',
    'mycelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'subnet_project.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'subnet_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'subnetPing',
#         'USER': 'postgres',
#         'PASSWORD': '123qwe',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'subnetPing',
        'USER': 'postgres',
        'PASSWORD': '123qwe',
        'HOST': 'db',
        'PORT': '5432',
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",  # Redis servisi adını ve portunu kullanın
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "cached"
    }
}
celery_app = Celery('subnet_project')

# Redis ayarları

CELERY_BROKER_URL = 'redis://redis:6379/1'  # Redis bağlantı URL'sini projenizin ayarlarına uygun şekilde güncelleyin.
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'  # Sonuçları saklamak için Redis'i kullanın, bağlantı bilgilerini güncelleyin.

app = Celery('subnet_project')  # Uygulamanızın adını burada kullanın
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# celery_app.conf.broker_url = 'redis://redis:6379/1'  # Redis bağlantı URL'sini projenizin ayarlarına uygun şekilde güncelleyin.
#
# # Autodiscover tasks.py dosyalarını
# celery_app.autodiscover_tasks()

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Herkese izin ver
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'