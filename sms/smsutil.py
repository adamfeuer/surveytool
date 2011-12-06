import os, time
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from sms.models import Setting

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

   def send(self, message, phoneNumber):
      phoneNumberWithPlus = "+" + phoneNumber
      try:
         message = self.client.sms.messages.create(to=phoneNumberWithPlus,
                                                   from_=self.fromPhoneNumber,
                                                   body=message)
      except TwilioRestException as e:
         error_message = "'%s'" % e
         return SmsStatus(SmsStatus.ERROR, error_message)
      return SmsStatus(SmsStatus.OK, message.status)
