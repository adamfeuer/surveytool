from django.conf import settings

def flavor_is_prod():
   return settings.FLAVOR == settings.PROD

def flavor_is_not_prod():
   return not (settings.FLAVOR == settings.PROD)
