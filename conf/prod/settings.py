import ConfigParser
from  surveytool.settings import *

LOGFILE_PATH = '/opt/webapps/surveytool/logs/surveytool.log'

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

DATABASES = {  
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/opt/webapps/surveytool/surveytool/surveytool.db',
        'TEST_NAME': ':memory:',
    }
}
# Key Czar and django-extensions
ENCRYPTED_FIELD_KEYS_DIR = '/opt/webapps/surveytool/surveytool/keys'

# SurveyTool settings
#FLAVOR = DEV
#DEBUG = False
#TEMPLATE_DEBUG = False

FLAVOR = DEV
DEBUG = True
TEMPLATE_DEBUG = True

#ALLOWED_PHONE_NUMBERS = []
ALLOWED_PHONE_NUMBERS = ['206-330-4774']

SURVEYTOOL_CONFIG = '/opt/webapps/surveytool/surveytool.config'
config = ConfigParser.RawConfigParser()
config.read(SURVEYTOOL_CONFIG)
TWILIO_FROM_PHONE_NUMBER = config.get('Twilio', 'TWILIO_FROM_PHONE_NUMBER')
TWILIO_ACCOUNT = config.get('Twilio', 'TWILIO_ACCOUNT')
TWILIO_TOKEN = config.get('Twilio', 'TWILIO_TOKEN')

