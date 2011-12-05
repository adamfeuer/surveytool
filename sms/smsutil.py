import os
from twilio.rest import TwilioRestClient
from sms.models import Setting

class SmsSender:
   def __init__(self):
      #self.fromPhoneNumber = Setting.objects.get(name='twilio_from_phone_number').value
      #account = Setting.objects.get(name='twilio_account').value
      #token = Setting.objects.get(name='twilio_token').value
      self.fromPhoneNumber = os.environ['TWILIO_FROM_PHONE_NUMBER']
      account = os.environ['TWILIO_ACCOUNT']
      token = os.environ['TWILIO_TOKEN']
      self.client = TwilioRestClient(account, token)

   def send(self, message, phoneNumber):
      phoneNumberWithPlus = "+" + phoneNumber
      message = self.client.sms.messages.create(to=phoneNumberWithPlus,
                                     from_=self.fromPhoneNumber,
                                     body=message)
      return message.status
      
