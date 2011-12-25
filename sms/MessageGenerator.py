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
      self.dayStart = datetime(self.start.year, self.start.month, self.start.day, dayStart.hour, dayStart.minute)
      self.updateDayLength()

   def setDayEnd(self, dayEnd):
      self.dayEnd = datetime(self.start.year, self.start.month, self.start.day, dayEnd.hour, dayEnd.minute)
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
      return segments


   def getDaysBetweenDates(self, startDateTime, endDateTime):
      thisDay = datetime(startDateTime.year, startDateTime.month, startDateTime.day)
      oneDay = timedelta(days = 1)
      days = 0
      while (thisDay < endDateTime):
         thisDay += oneDay
         days += 1
      return days
