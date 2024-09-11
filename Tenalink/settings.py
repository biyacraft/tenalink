from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-5tzupl#d@sea(h7c@@=x$876qo*$0(3_u3unb@&%!$9a4dxb30'

DEBUG = True

ALLOWED_HOSTS = [
    '.vercel.app',
    'now.sh',
    'localhost',
    '127.0.0.1',
    'da87-102-218-51-253.ngrok-free.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://da87-102-218-51-253.ngrok-free.app/',

]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'account',
    'dashboard',
    'appointment',
    'webrtc',
    'recommendation',

    'mathfilters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # new

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'Tenalink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'Tenalink.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:qUoZzcbtgBtAyqaeEPbDFSaJMomoxXxq@junction.proxy.rlwy.net:56537/railway',
        conn_max_age=600,
        ssl_require=True,
    )
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ayalkbettesfahun@gmail.com'
EMAIL_HOST_PASSWORD = 'vpajumtxbwwgtpbt'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ayalkbettesfahun@gmail.com'


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
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    'https://1c25-196-189-233-4.ngrok-free.app'
]
CORS_ALLOWED_ORIGINS = [
    'https://1c25-196-189-233-4.ngrok-free.app'
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
