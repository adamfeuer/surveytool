import time, logging, string
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from django.conf import settings
from surveytool.common.util import flavor_is_not_prod

logger = logging.getLogger(__name__)

class SmsStatus:
   OK = True
   ERROR = False
   def __init__(self, status, message):
      self.status = status
      self.message = message

class SmsSender:
   def __init__(self):
      self.fromPhoneNumber = settings.TWILIO_FROM_PHONE_NUMBER
      account = settings.TWILIO_ACCOUNT
      token = settings.TWILIO_TOKEN
      self.client = TwilioRestClient(account, token)

   def removeDashes(self, phoneNumber):
        return phoneNumber.replace('-', '')

   def format(self, phoneNumber):
      if (phoneNumber[0] == "1"):
          prefix = "+"
      else:
          prefix =  "+1"
      phoneNumber = self.removeDashes(phoneNumber)
      return prefix + phoneNumber

   def send(self, phoneNumber, message):
      if (flavor_is_not_prod() and phoneNumber not in settings.ALLOWED_PHONE_NUMBERS): 
         status = "Not sending message because the phone number is not in ALLOWED_PHONE_NUMBERS."
         logger.warn(status)
         return SmsStatus(SmsStatus.ERROR, status)
      phoneNumberWithPlus = self.format(phoneNumber)
      try:
         message = self.client.sms.messages.create(to=phoneNumberWithPlus,
                                                   from_=self.fromPhoneNumber,
                                                   body=message)
         logger.info("Sent message to %s." % phoneNumber)
      except TwilioRestException as e:
         error_message = "'%s'" % e
         logger.error("Twilio error: %s" % error_message)
         return SmsStatus(SmsStatus.ERROR, error_message)
      return SmsStatus(SmsStatus.OK, message.status)

