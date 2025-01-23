import dj_database_url
from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Secret Key
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
# ALLOWED_HOSTS = ['127.0.0.1','https://junction-dental.onrender.com/', 'congenial-sniffle-jwwvxwq549pf5r57-8000.app.github.dev']
ALLOWED_HOSTS = ['*']
# DEBUG = config('DEBUG', default=False, cast=bool)
#
# DEBUG = True
# ALLOWED_HOSTS = ['https://junction-dental.onrender.com/', '*']


INSTALLED_APPS = [
  
    'Junction_Dental',
    'django_browser_reload',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'sendsms',
    'africastalking',

    'Accounts',
    'channels',
    'Clinic',
    'Appointment',
    'Dashboard',
    'doctors',
    'bookings',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # Required for social authentication
    'allauth.socialaccount.providers.google',  # Add other providers as needed


    
    

]

SITE_ID = 1

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'Junction_Dental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'Templates')],
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

WSGI_APPLICATION = 'Junction_Dental.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Replace the SQLite DATABASES configuration with PostgreSQL:

# DATABASES = {
#     'default': dj_database_url.config(
#         # Replace this value with your local database's connection string.
#         default='postgresql://mboa_technologies:Lo0jfbPff0gXDsGDms69iCwOMzOautRY@dpg-cu4j6trqf0us7382on7g-a/junction_dental_clinic',
#         conn_max_age=600
#     )
# }

# DATABASES = {
#     'default': dj_database_url.config(
#         # Replace this value with your local database's connection string.
#         default='postgresql://junction_dental_db_user:LucwTNQzdL1ibqUSLcbcmNmhHF8u1Dsq@dpg-cu20u9ogph6c73em3fcg-a/junction_dental_db',
#         conn_max_age=600
#     )
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default
    'allauth.account.auth_backends.AuthenticationBackend', ] # Added for allauth

AUTH_USER_MODEL = 'Accounts.User'

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '1002135850953-mt52t7sl6cfl4dh0a7e9u79v9sv7rben.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

LOGIN_REDIRECT_URL = '/accounts/profile'
ACCOUNT_SIGNUP_REDIRECT_URL = 'accounts/profile'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = ['https://junction-dental.onrender.com',  'http://127.0.0.1:8000']

# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
# twillio Account Recovery CYLFDTYXGFV38LMFXFXJM4S6
SENDSMS_BACKEND = 'Junction_Dental.mysmsbackend.SmsBackend'

# Email configuration
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Options: "none", "optional", "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # Options: "username", "email", "username_email"
ACCOUNT_USERNAME_REQUIRED = True


TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Example: Gmail's SMTP server
EMAIL_PORT = 587  # TLS port
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mboaacademy@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'cnwuqmdvzejeojyi'  # Your email password (use app-specific passwords for Gmail or similar)

BROWSER_RELOAD = False

API_KEY = config('API_KEY')
API_USERNAME = config('API_USERNAME')
