import os, sys

abspath = lambda *p: os.path.abspath(os.path.join(*p))

PROJECT_ROOT = abspath(os.path.dirname(__file__))
USERENA_MODULE_PATH = abspath(PROJECT_ROOT, '..')
sys.path.insert(0, USERENA_MODULE_PATH)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Adam Feuer', 'adamf@pobox.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'surveytool.db',
        'TEST_NAME': ':memory:',
    }
}

if DEBUG:
    # Use the Python SMTP debugging server. You can run it with:
    # ``python -m smtpd -n -c DebuggingServer localhost:1025``.
    EMAIL_PORT = 1025

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = abspath(PROJECT_ROOT, 'media')
DOCUMENT_ROOT = abspath(PROJECT_ROOT, 'docs')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'sx405#tc)5m@s#^jh5l7$k#cl3ekg)jtbo2ds(n(kw@gp0t7x@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/surveytool2-email.log' 

ROOT_URLCONF = 'surveytool.urls'

TEMPLATE_DIRS = (
    abspath(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'easy_thumbnails',
    'guardian',
    'south',
    'userena',
    'userena.contrib.umessages',
    'cronjobs',
    'surveytool.profiles',
    'surveytool.sms',

)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/surveytool.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'request_handler': {
                'level':'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': 'logs/django_request.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

# Userena settings
USERENA_ACTIVATION_REQUIRED = False
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
AUTH_PROFILE_MODULE = 'profiles.Profile'
USERENA_WITHOUT_USERNAME = True
USERENA_DISABLE_PROFILE_LIST = True
USERENA_MUGSHOT_SIZE = 140

# Test settings
TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# Guardian
ANONYMOUS_USER_ID = -1

# Key Czar and django-extensions
ENCRYPTED_FIELD_KEYS_DIR = 'keys'

# Survey Tool

PROD = "prod"
TEST = "test"
DEV = "dev"


