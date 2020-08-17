import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TESTING = sys.argv[1:2] == ['test']
SHELL = 'shell' in sys.argv or 'shell_plus' in sys.argv

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'flat-json-widget.db'}
}

SECRET_KEY = 'fn)t*+$)ugeyip6-#txyy$5wf2ervc0d2n#h)qb)y5@ly$t*@w'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.admin',
    'flat_json_widget',
    'test_app'
    # 'debug_toolbar',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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

if 'debug_toolbar' in INSTALLED_APPS:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'urls'

TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-gb'
USE_TZ = True
USE_I18N = False
USE_L10N = False
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = f'{os.path.dirname(BASE_DIR)}/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'openwisp_utils.loaders.DependencyLoader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

LOGIN_REDIRECT_URL = 'admin:index'

# during development only
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'filters': {'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
}

if not TESTING and SHELL:
    LOGGING.update(
        {
            'loggers': {
                '': {
                    # this sets root level logger to log debug and higher level
                    # logs to console. All other loggers inherit settings from
                    # root level logger.
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
                'django.db': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
            }
        }
    )

TEST_RUNNER = 'openwisp_utils.tests.TimeLoggingTestRunner'
