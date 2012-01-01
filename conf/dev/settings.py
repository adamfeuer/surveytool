from  surveytool.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'surveytool.db',
        'TEST_NAME': ':memory:',
    }
}

# Key Czar and django-extensions
ENCRYPTED_FIELD_KEYS_DIR = 'keys'

# SurveyTool settings
FLAVOR = DEV
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_PHONE_NUMBERS = ['206-330-4774']
#ALLOWED_PHONE_NUMBERS = []

