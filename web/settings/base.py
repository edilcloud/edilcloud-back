# -*- coding: utf-8 -*-

import os
import datetime

import filetype
from filetype.types import Type as EdilType

gettext = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))
)

SETTINGS_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_PATH = os.path.dirname(SETTINGS_PATH)

BASE_SITE_DOMAIN = 'www.whistle.it'

LOGIN_URL = '/admin/login/'

APPEND_SLASH = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1']

ADMIN_LANGUAGE_CODE = 'it'

DEVELOPERS = [
    'tbellini@edilcloud.io'
]
# Application definition

INSTALLED_APPS = [
    'flat_responsive',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django_extensions',
    'debug_toolbar',
    #'mptt',

    'rest_framework_docs',

    'rest_framework',
    'rest_framework.authtoken',

    'social_django',
    'rest_social_auth',

    'rest_auth', # Todo: Before removing this package, you must create custom serializers for PasswordChange, Reset etc

    'web',
    'apps.document.apps.DocumentConfig',
    'apps.media.apps.MediaConfig',
    'apps.menu.apps.MenuConfig',
    'apps.message.apps.MessageConfig',
    'apps.notify.apps.NotifyConfig',
    'apps.product.apps.ProductConfig',
    'apps.profile.apps.ProfileConfig',
    'apps.project.apps.ProjectConfig',
    'apps.quotation.apps.QuotationConfig',
    'apps.user.apps.UserConfig',
    'apps.pushpin.apps.PushpinConfig',
    'corsheaders',
    'channels',
    'apps.ws'
]
ASGI_APPLICATION = "web.routing.application"
CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            "hosts": [('redis', 6379)],
        }
    },
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_IMPORTS = ['web.tasks',]
CELERY_BEAT_SCHEDULE = {
    'printHello': {
        'task': 'web.tasks.archived_projects_reminder',
        'schedule': 86400.0,
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.core.middleware.thread_local.ThreadLocalMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, "templates")],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]

        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'web', 'locale'),
)
LANGUAGES = (
    ('it', gettext('Italian')),
    ('en', gettext('English')),
)

OWNER = 'o'
DELEGATE = 'd'
LEVEL_1 = 'm'
LEVEL_2 = 'w'
MEMBERS = [OWNER, DELEGATE, LEVEL_1, LEVEL_2]

# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web", "static"),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'exceptions': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/django/whistle-exceptions.log',
            'level': 'DEBUG',
        },
        'api_exceptions': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/django/whistle-api_exceptions.log',
        },
        'import': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/django/whistle.import.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/django/whistle.log',
            'level': 'INFO',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        # tail -f /var/log/django/whistle-exceptions.log
        'exceptions': {
            'handlers': ['exceptions'],
            'level': 'DEBUG',
        },
        # tail -f /var/log/django/whistle-api_exceptions.log
        'api_exceptions': {
            'handlers': ['api_exceptions'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'console': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # tail -f /var/log/django/whistle.log
        'file': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'email': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
        },
        'import_generic': {
            'handlers': ['import'],
            'level': 'INFO',
        }
    }
}

# django rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'web.api.pagination.ThuxPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'EXCEPTION_HANDLER': 'web.drf.exceptions.whistle_exception_handler'
}
REST_FRAMEWORK_PAGE_SIZE_QUERY_PARAM = 'per_page'

# REST_AUTH_SERIALIZERS = {
#     "PASSWORD_RESET_SERIALIZER": "web.serializers.PasswordResetSerializer"
# }

DJANGO_ADMIN_LIST_PER_PAGE = 10

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

WHISTLE_CRONTAB_USERNAME = '< set in local.py >'

# SOCIAL AUTH SETTINGS
SOCIAL_AUTH_FACEBOOK_KEY = '< set in local.py >'
SOCIAL_AUTH_FACEBOOK_SECRET = '< set in local.py >'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '< set in local.py >'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '< set in local.py >'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '< set in local.py >'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = '< set in local.py >'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': ','.join([
        'id', 'cover', 'name', 'first_name',
        'last_name', 'age_range', 'link',
        'gender', 'locale', 'picture',
        'timezone', 'updated_time',
        'verified', 'email',
    ]),
}

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address']
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('firstName', 'first_name'),
    ('lastName', 'last_name'),
    ('emailAddress', 'email_address')
]

# SOCIALACCOUNT_PROVIDERS = {
#
#     'facebook': {
#         'METHOD': 'oauth2',
#         'SCOPE': ['email', 'public_profile', 'user_friends'],
#         'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
#         'INIT_PARAMS': {'cookie': True},
#         'FIELDS': [
#             'id',
#             'email',
#             'name',
#             'first_name',
#             'last_name',
#             'verified',
#             'locale',
#             'timezone',
#             'link',
#             'gender',
#             'updated_time',
#         ],
#         'EXCHANGE_TOKEN': True,
#         'LOCALE_FUNC': lambda request: 'en_US',
#         'VERIFIED_EMAIL': False,
#     },
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     },
#     'linkedin_oauth2': {
#         'SCOPE': [
#             'r_emailaddress',
#         ],
#         'PROFILE_FIELDS': [
#             'id',
#             'first-name',
#             'last-name',
#             'email-address',
#             'picture-url',
#             'public-profile-url',
#         ]
#     }
# }

BASE_URL = 'test.edilcloud.io'

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'apps.user.views.custom_jwt_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.user.views.custom_jwt_response_payload_handler',
    'JWT_LEEWAY': 100,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=1000),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

REST_USE_JWT = True

SOCIALACCOUNT_EMAIL_VERIFICATION = None
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True

# Allauth Settings
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False

# Custom Adapter for whistle authentication

# SOCIALACCOUNT_ADAPTER = 'web.adapter.SocialAccountAdapter'
# ACCOUNT_ADAPTER = 'web.adapter.AccountAdapter'

# CROSS ORIGIN RESOURCE SHARING
CORS_ORIGIN_WHITELIST = (
    # List of Domain we want to allow
    'http://ec2-3-9-170-59.eu-west-2.compute.amazonaws.com:8000',
    'http://localhost:3000',
    'https://www.edilcloud.ml',
    'https://www.back.edilcloud.ml'
)
CORS_ORIGIN_ALLOW_ALL = True  # For now Allow ALL
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
)

FAKER_LOCALE = None
FAKER_PROVIDERS = None


UPLOAD_FILE_PATH = os.path.join(BASE_DIR, 'media')

PROTOCOL = 'https'
DEFAULT_FROM_EMAIL = 'notification@edilcloud.io'
REGISTRATION_FROM_EMAIL = 'registration@edilcloud.io'
REGISTRATION_EMAIL_HOST_PASSWORD = 'MonkeyBits2020'
SERVER_EMAIL = 'mail.edilcloud.io'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.edilcloud.io'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'notification@edilcloud.io'
EMAIL_HOST_PASSWORD = 'MonkeyBits2020'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

NEW_SPONSOR_REQUEST_RECIPIENT = 'edilcloud.activation@gmail.com'

# override filetype package adding new types
class Dwg(EdilType):
    """
    Implements the Zip archive type matcher.
    """
    MIME = 'image/vnd'
    EXTENSION = 'dwg'

    def __init__(self):
        super(Dwg, self).__init__(
            mime=Dwg.MIME,
            extension=Dwg.EXTENSION
        )

    def match(self, buf):
        return (len(buf) > 3 and
                buf[0] == 0x50 and buf[1] == 0x4B and
                (buf[2] == 0x3 or buf[2] == 0x5 or
                    buf[2] == 0x7) and
                (buf[3] == 0x4 or buf[3] == 0x6 or
                    buf[3] == 0x8))
#filetype.types.insert(0, Dwg)
