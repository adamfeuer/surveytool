import logging, sys, datetime
import cronjobs

from models import Message
from SmsSender import SmsSender, SmsStatus

logger = logging.getLogger(__name__)

TOO_OLD_MINUTES = 5

@cronjobs.register
def send_messages():
   message_sender = SmsSender()
   now = datetime.datetime.now()
   now_string = now.strftime("%Y-%m-%d %H:%M")
   max_timedelta = datetime.timedelta(minutes = TOO_OLD_MINUTES)
   messages = Message.objects.filter(send_at__lte=now_string).exclude(sent=True).order_by('send_at')
   for message in messages:
      delta = now - message.send_at
      if delta > max_timedelta:
         error_message = "Not sending message since it is more than %s old. [%s:%s %s - %s]" % (max_timedelta, message.id, message.send_at, message.phone_number, message.message)
         logger.info(error_message)
         message.sent = True
         message.sent_status = SmsStatus.ERROR
         message.sent_error_message = error_message
      else:
         logger.info("sending message %s:%s %s - %s" % (message.id, message.send_at, message.phone_number, message.message))
         status = message_sender.send(message.phone_number, message.message)
         message.sent = status.status
         message.sent_status = status.status
         message.sent_error_message = status.message
         logger.info("Sent message %s:%s %s %s" % (message.id, message.phone_number, message.sent_status, message.sent_error_message))
      message.save()

      
      
