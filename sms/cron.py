import sys, datetime
import cronjobs

from models import Message
from smsutil import SmsSender

@cronjobs.register
def send_messages():
   message_sender = SmsSender()
   now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
   messages = Message.objects.filter(send_at__lte=now).exclude(sent=True).order_by('send_at')
   for message in messages:
      print "sending message %s:%s %s - %s" % (message.id, message.send_at, message.phone_number, message.message)
      status = message_sender.send(message.phone_number, message.message)
      message.sent = status.status
      message.sent_status = status.status
      message.sent_error_message = status.message
      message.save()
      print "Sent message %s:%s %s %s" % (message.id, message.phone_number, message.sent_status, message.sent_error_message)

      
      
