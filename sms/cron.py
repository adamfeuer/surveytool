import sys
import cronjobs

@cronjobs.register
def send_messages_task():
   print "Hello, World!"

