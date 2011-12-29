import math, random, logging, string
from datetime import time, datetime, timedelta
from django.conf import settings

from sms.models import Message, UserDetail
from common.util import num_encode

logger = logging.getLogger(__name__)

DEFAULT_SALUTATION = ""
TIME_FORMAT = "%Y-%m-%d %H:%M"
MAXIMUM_RANDOM_ID = 999999999

class DaySegment:
   def __init__(self, startDateTime, segmentLength, dayStart, dayEnd):
      self.segmentLength = segmentLength
      self.start = startDateTime
      self.end = startDateTime + segmentLength - timedelta(days=0, seconds=1)
      self.dayStart = datetime(self.start.year, self.start.month, self.start.day, dayStart.hour, dayStart.minute)
      self.dayEnd  = datetime(self.start.year, self.start.month, self.start.day, dayEnd.hour, dayEnd.minute)
      self.updateDayLength()

   def updateDayLength(self):
      self.dayLength = self.dayEnd - self.dayStart

   def setDayStart(self, dayStart):
      self.dayStart = dayStart
      self.updateDayLength()

   def setDayEnd(self, dayEnd):
      self.dayEnd = dayEnd
      self.updateDayLength()

class MessageGenerator:
   def __init__(self):
      pass

   def getDaySegmentsForDates(self, startDateTime, endDateTime, dayStart, dayEnd):
      segments = []
      thisDay = datetime(startDateTime.year, startDateTime.month, startDateTime.day)
      oneDay = timedelta(days = 1)
      while (thisDay < endDateTime):
         newSegment = DaySegment(thisDay, oneDay, dayStart, dayEnd)
         thisDay += oneDay
         segments.append(newSegment)
      self.fixFirstDay(segments, startDateTime)
      self.fixLastDay(segments, endDateTime)
      return segments

   def fixFirstDay(self, segments, startDateTime):
      segment = segments[0]
      if (segment.dayStart < startDateTime):
         segment.setDayStart(startDateTime)

   def fixLastDay(self, segments, endDateTime):
      segment = segments[-1]
      if (endDateTime < segment.dayEnd):
         segment.setDayEnd(endDateTime)

   def getNumberOfMessagesForSegment(self, segment, messagesPerDay, dayLength):
      dayLengthInSeconds = dayLength.total_seconds()
      messagesPerSecond = float(messagesPerDay) / float(dayLengthInSeconds)
      result = int(messagesPerSecond * segment.dayLength.total_seconds())
      return result

   def getMessageAtRandomTimeInInterval(self, index, intervalLengthInSeconds):
      return (index * intervalLengthInSeconds) + random.randint(0, intervalLengthInSeconds)

   def getMessageDateTime(self, dayStart, messageSeconds):
      return dayStart + timedelta(seconds = messageSeconds)
      
   def getMessageDateTimesForSegment(self, segment, messagesPerDay, dayLength, guardTimeMinutes):
      """
      Returns a list of DateTime objects that correspond to random message times for
      that DaySegment.
      
      For more info on the algorithm, see:
   
      Validity and Reliability of the Experience-Sampling Method
      Mihaly Csikszentmihalyi, Reed Larson	 (1987)
      The Journal of Nervous and Mental Disease	 175 (9)	 p. 528

      """
      messagesForSegment = self.getNumberOfMessagesForSegment(segment, messagesPerDay, dayLength)
      intervalLengthInSeconds = int(segment.dayLength.total_seconds() / messagesForSegment)
      guardTimeInSeconds = guardTimeMinutes * 60
      interval = 0
      messageDateTimes = []
      messageSeconds = self.getMessageAtRandomTimeInInterval(interval, intervalLengthInSeconds)
      messageDateTimes.append(self.getMessageDateTime(segment.dayStart, messageSeconds))
      while (interval < messagesPerDay):
         interval += 1
         newMessageSeconds = self.getMessageAtRandomTimeInInterval(interval, intervalLengthInSeconds)
         if ((newMessageSeconds - messageSeconds) < guardTimeInSeconds):
            newMessageSeconds += guardTimeInSeconds
         messageDateTime = self.getMessageDateTime(segment.dayStart, newMessageSeconds)
         if (messageDateTime <= segment.dayEnd):
            messageDateTimes.append(messageDateTime)
         messageSeconds = newMessageSeconds
      return messageDateTimes

   def getDayLength(self, dayStart, dayEnd):
      now = datetime.now()
      start = datetime(now.year, now.month, now.day, hour=dayStart.hour, minute=dayStart.minute, second=dayStart.second)
      end = datetime(now.year, now.month, now.day, hour=dayEnd.hour, minute=dayEnd.minute, second=dayEnd.second)
      return end - start

   def getMessageDateTimesForProject(self, start, end, dayStart, dayEnd, messagesPerDay, guardTimeMinutes):
      dayLength = self.getDayLength(dayStart, dayEnd)
      messageDateTimes = []
      segments = self.getDaySegmentsForDates(start, end, dayStart, dayEnd)
      for segment in segments:
         messageDateTimes += self.getMessageDateTimesForSegment(segment, messagesPerDay, dayLength, guardTimeMinutes)
      return messageDateTimes

   def getMessageText(self, user, userDetail, project, identifier):
      allowed_variables = {
         'first' : user.first_name,
         'last': user.last_name,
         'url':project.survey_url,
         'id' : identifier,
         }
      if (userDetail.smartphone is True):
         message_base = project.smartphone_message 
      else:
         message_base = project.text_message
      return message_base % allowed_variables

   def getIdentifier(self, project, user):
      identifier_num = int("%d%d%d" % (project.id, user.id, random.randint(0,MAXIMUM_RANDOM_ID)))
      return num_encode(identifier_num)
      
   def generateMessage(self, user, project, messageDateTime):
      # todo - defaults if fields are not filled out, message validation
      userDetailList = UserDetail.objects.filter(user__id = user.id)
      userDetail = userDetailList[0]
      if (userDetail.no_messages is True):
         logger.warn("INFO: not sending message to user %s because no_messages is True." % user.id)
         return
      message = Message()
      message.project = project
      message.user_id = "%s" % user.id
      message.identifier = self.getIdentifier(project, user)
      message.phone_number = "%s" % userDetail.phone_number
      message.send_at = messageDateTime.strftime(TIME_FORMAT)
      message.message = self.getMessageText(user, userDetail, project, message.identifier)
      message.save()

   def generateMessages(self, user, project):
      messageDateTimes = self.getMessageDateTimesForProject(project.start_datetime, project.end_datetime,
                                                            project.day_start_time, project.day_end_time,
                                                            project.messages_per_day, project.guard_time_minutes)
      for messageDateTime in messageDateTimes:
         self.generateMessage(user, project, messageDateTime)


