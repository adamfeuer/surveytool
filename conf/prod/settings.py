from  surveytool.settings import *

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

