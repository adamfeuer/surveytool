import ConfigParser
from  surveytool.settings import *

SURVEYTOOL_CONFIG = '/opt/webapps/research-staging.liveingreatness.com/surveytool.config'
config = ConfigParser.RawConfigParser()
config.read(SURVEYTOOL_CONFIG)
TWILIO_FROM_PHONE_NUMBER = config.get('Twilio', 'TWILIO_FROM_PHONE_NUMBER')
TWILIO_ACCOUNT = config.get('Twilio', 'TWILIO_ACCOUNT')
TWILIO_TOKEN = config.get('Twilio', 'TWILIO_TOKEN')
DATABASE_HOST = config.get('Database', 'host')
DATABASE_USER = config.get('Database', 'user')
DATABASE_PASSWORD = config.get('Database', 'password')
DATABASE_DB = config.get('Database', 'database')

BASE_URL="http://research-staging.liveingreatness.com"

STATIC_ROOT = '/opt/webapps/research-staging.liveingreatness.com/surveytool/static'
STATIC_URL = '/static/'
LOGFILE_PATH = '/opt/webapps/research-staging.liveingreatness.com/logs/surveytool.log'

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
            'filename': LOGFILE_PATH,
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
                'level':'INFO',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/apache2/research-staging.liveingreatness-django-request.log',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_DB,
        'ENGINE': 'postgresql_psycopg2',
        'HOST': DATABASE_HOST,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        }
}

# Key Czar and django-extensions
ENCRYPTED_FIELD_KEYS_DIR = '/opt/webapps/research-staging.liveingreatness.com/surveytool/keys'

# SurveyTool settings
FLAVOR = PROD
DEBUG = False
TEMPLATE_DEBUG = False

CRONJOB_LOCK_PREFIX = 'lock.staging'

#FLAVOR = DEV
#DEBUG = True
#TEMPLATE_DEBUG = True

ALLOWED_PHONE_NUMBERS = []
#ALLOWED_PHONE_NUMBERS = ['206-330-4774']

