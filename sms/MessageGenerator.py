from datetime import time, datetime, timedelta

class DaySegment:
   def __init__(self, startDateTime, segmentLength):
      self.segmentLength = segmentLength
      self.start = startDateTime
      self.end = startDateTime + segmentLength
      self.dayStart = None
      self.dayEnd = None

class MessageGenerator:
   def __init__(self):
      pass

   def getDaySegmentsForDates(self, startDateTime, endDateTime):
      segments = []
      thisDay = datetime(startDateTime.year, startDateTime.month, startDateTime.day)
      oneDay = timedelta(1)
      days = 0
      while (thisDay < endDateTime):
         newSegment = DaySegment(thisDay, oneDay)
         thisDay += oneDay
         days += 1
         segments.append(newSegment)
      return segments

   def getDaysBetweenDates(self, startDateTime, endDateTime):
      thisDay = datetime(startDateTime.year, startDateTime.month, startDateTime.day)
      oneDay = timedelta(1)
      days = 0
      while (thisDay < endDateTime):
         thisDay += oneDay
         days += 1
      return days
