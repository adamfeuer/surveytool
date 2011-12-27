import os, time
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from django.conf import settings

class SmsStatus:
   OK = True
   ERROR = False
   def __init__(self, status, message):
      self.status = status
      self.message = message

class SmsSender:
   def __init__(self):
      self.fromPhoneNumber = os.environ['TWILIO_FROM_PHONE_NUMBER']
      account = os.environ['TWILIO_ACCOUNT']
      token = os.environ['TWILIO_TOKEN']
      self.client = TwilioRestClient(account, token)

   def send(self, phoneNumber, message):
      if phoneNumber not in settings.ALLOWED_PHONE_NUMBERS: 
         status = "INFO: not sending message because the phone number is not in ALLOWED_PHONE_NUMBERS."
         print status
         return SmsStatus(SmsStatus.ERROR, status)
      phoneNumberWithPlus = "+" + phoneNumber
      try:
         message = self.client.sms.messages.create(to=phoneNumberWithPlus,
                                                   from_=self.fromPhoneNumber,
                                                   body=message)
      except TwilioRestException as e:
         error_message = "'%s'" % e
         return SmsStatus(SmsStatus.ERROR, error_message)
      return SmsStatus(SmsStatus.OK, message.status)
