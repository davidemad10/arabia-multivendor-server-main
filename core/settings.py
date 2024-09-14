
from datetime import timedelta
from pathlib import Path
import environ 
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from django.utils.translation import gettext_lazy as _


env=environ.Env()
# env_file = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = 'django-insecure-t+o87tcbcea5%kkscv($!=5js%-@sxk7wq1v%tdjg$njj5$h^%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local Apps
    'account',
    'dashboard',
    'product',
    'order',
    'advertisement',
    # 3rd Party Apps
    # "django_extensions",
    "django_filters",

    "drf_yasg",
    "rest_framework",
    # "taggit",
    "corsheaders",
    "rosetta",
    "parler",
    "mptt",
    "modeltranslation",
    "rest_framework_swagger"
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',#الخاص بالترجمة
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}




SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=190),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "ROTATE_REFRESH_TOKENS": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


FRONTEND_URL='http://localhost:5173'

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]
CORS_ALLOW_ALL_ORIGINS=True



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',#ترجمة
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
AUTH_USER_MODEL = 'account.User'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': env("DB_NAME"),
'USER': env("DB_USER"),
'PASSWORD': env("DB_PASSWORD"),
'HOST': env("DB_HOST"),
'PORT': env("DB_PORT"), 
}
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [os.path.join(BASE_DIR,'locale')]

LANGUAGES = (
    ("en", _("English")),
    ("ar", _("Arabic")),
)
PARLER_LANGUAGES = {
    None: (
        {'code': 'en',},
        {'code': 'ar',},

    ),
    'default': {
        'fallbacks': ['en'],         
        'hide_untranslated': False,   
    }
}

USE_TZ = True




STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # "/var/www/static/",
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "sistar32.m@gmail.com"
EMAIL_HOST_PASSWORD = "usws cxac oqec tuqi"
EMAIL_USE_TLS = True





CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000"
]
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"

