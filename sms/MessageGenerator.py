import math
from datetime import time, datetime, timedelta

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
      
