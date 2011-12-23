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

   def getDaySegments(self, startDateTime, endDateTime):
      segment = DaySegment(startDateTime, endDateTime-startDateTime)
      return [segment, segment, segment]


   def getDaysBetweenDates(self, startDateTime, endDateTime):
      thisDay = datetime(startDateTime.year, startDateTime.month, startDateTime.day)
      oneDay = timedelta(1)
      days = 0
      while (thisDay < endDateTime):
         thisDay += oneDay
         days += 1
      return days - 1
