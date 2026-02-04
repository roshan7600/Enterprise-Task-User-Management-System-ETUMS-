from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ensure logs directory exists
LOG_DIR = BASE_DIR / 'logs'
try:
    LOG_DIR.mkdir(exist_ok=True)
    print(f"✓ Logs directory created/verified at: {LOG_DIR}")
except Exception as e:
    print(f"⚠ Warning: Could not create logs directory: {e}")

# SECURITY
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "accounts.User"

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'apps.accounts.apps.AccountsConfig',
    'apps.tasks.apps.TasksConfig',
    'apps.core.apps.CoreConfig',
    'django_extensions',
    'django_filters',
    'drf_spectacular',
]

# MIDDLEWARE (REQUIRED FOR ADMIN & AUTH)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL CONFIG
ROOT_URLCONF = 'etums.urls'

# TEMPLATES (REQUIRED FOR ADMIN)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# WSGI
WSGI_APPLICATION = 'etums.wsgi.application'

# DATABASE (MYSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# STATIC FILES
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST FRAMEWORK DRF configuration:

REST_FRAMEWORK = {
    # 🔐 Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    # 🛡️ Permissions
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    # 🚦 Throttling (Rate Limiting)
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "user": "100/hour",
        "anon": "20/hour",
        "login": "5/min",   # 🔒 Login protection
    },

    # 📄 Pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,

    # 📘 API Schema (Swagger / OpenAPI)
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}




# JWT settings

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       

    }
}

# ENABLE SECURITY HEADERS

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

CSRF_COOKIE_SECURE = False   # True in production (HTTPS)
SESSION_COOKIE_SECURE = False

# LOGGING configuration



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/app.log"),
            "formatter": "verbose",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    },
}

LOGGING["loggers"]["django.request"]["level"] = "WARNING"

LOGGING["loggers"]["django.server"] = {
    "handlers": ["file"],
    "level": "INFO",
    "propagate": False,
}


# SPECTACULAR SETTINGS

SPECTACULAR_SETTINGS = {
    "TITLE": "Enterprise Task & User Management API",
    "DESCRIPTION": "Production-ready backend system with JWT, RBAC, bulk operations, logging, and security.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    "COMPONENT_SPLIT_REQUEST": True,

    "SECURITY": [
        {
            "bearerAuth": []
        }
    ],
}
