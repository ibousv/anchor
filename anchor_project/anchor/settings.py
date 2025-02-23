import os
import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

env = environ.Env()
if os.path.exists(os.path.join(PROJECT_ROOT, ".env")):
    env.read_env(os.path.join(PROJECT_ROOT, ".env"))

# SEPS Activation
POLARIS_ACTIVE_SEPS = ["sep-1", "sep-10", "sep-24","sep-31"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_-y18fb649lc&@m79l+@g@(ewd$%anag6s+-jt8_=1ja^uv+*#'

MULT_ASSET_ADDITIONAL_SIGNING_SEED = env(
    "MULT_ASSET_ADDITIONAL_SIGNING_SEED", default=None
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
""" ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "[::1]", "0.0.0.0"]
) """

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    "rest_framework",
    "polaris",
    'anchor.apps.AnchorConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "polaris.middleware.TimezoneMiddleware",
]

local_mode = env.bool("LOCAL_MODE", default=False)

SESSION_COOKIE_SECURE = not local_mode # can be True for sep-24 deployment

SECURE_SSL_REDIRECT = not local_mode
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

APPEND_SLASH = False

ROOT_URLCONF = "anchor.urls"

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

WSGI_APPLICATION = 'anchor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:////" + os.path.join(BASE_DIR, "data/db.sqlite3"),
    )
}

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

STATIC_ROOT= os.path.join(BASE_DIR, 'collectstatic')
STATIC_URL= "/polaris/static/"
STATICFILES_STORAGE= "whitenoise.storage.CompressedManifestStaticFilesStorage"


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
    "PAGE_SIZE": 10,
}

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default=None)
EMAIL_USE_TLS = True
EMAIL_PORT = 587

CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "polaris": {
            "format": "{asctime} - {levelname} - {name}:{lineno} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
        "default": {
            "format": "{asctime} - {levelname} - {name} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
    },
    "handlers": {
        "polaris-console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "polaris",
        },
        "default-console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
        },
    },
    "loggers": {
        "server": {
            "handlers": ["polaris-console"],
            "propogate": False,
            "level": "INFO",
        },
        "polaris": {
            "handlers": ["polaris-console"],
            "propogate": False,
            "level": "DEBUG",
        },
        "django": {
            "handlers": ["default-console"],
            "propogate": False,
            "level": "INFO",
        },
    },
}
