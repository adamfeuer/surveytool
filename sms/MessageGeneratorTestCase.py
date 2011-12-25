from datetime import time, datetime, timedelta

from django.utils import unittest
from sms.MessageGenerator import MessageGenerator, DaySegment


class MessageGeneratorTestCase(unittest.TestCase):

   def setUp(self):
      self.messageGenerator = MessageGenerator()

   def testGetDaysBetweenDatesStartMidnight(self):
      startDateTime = datetime(2011, 12, 23, 0, 0, 0)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=1, expectedNumberOfDays=1)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=2, expectedNumberOfDays=2)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=3, expectedNumberOfDays=3)

   def testGetDaysBetweenDatesStartNotMidnight(self):
      startDateTime = datetime(2011, 12, 23, 9, 30, 0)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=1, expectedNumberOfDays=2)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=2, expectedNumberOfDays=3)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=3, expectedNumberOfDays=4)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=7, expectedNumberOfDays=8)

   def testGetDaySegmentsForDatesMidnight(self):
      startDateTime = datetime(2011, 12, 23, 0, 0, 0)
      self.verifyDaySegmentsForDates(startDateTime, surveyLengthInDays=1,
                                     expectedNumberOfDays=1)
      self.verifyDaySegmentsForDates(startDateTime, surveyLengthInDays=2,
                                     expectedNumberOfDays=2)
      self.verifyDaySegmentsForDates(startDateTime, surveyLengthInDays=3,
                                     expectedNumberOfDays=3)

   def testGetDaySegmentsContentsForDatesMidnight(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 23, 2, 10, 0)
      surveyLengthInDays=1
      expectedNumberOfDays=2
      surveyLength = timedelta(surveyLengthInDays)
      endDateTime = startDateTime + surveyLength
      dayStart = time(hour = 0, minute = 0, second = 0)
      dayEnd = time(hour = 23, minute = 59, second = 59)
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))
      segment = result[0]
      expectedDayStart = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedDayStart, segment.dayStart, "dayStart should be identical: %s - %s" % (dayStart, segment.dayStart))


   def testGetDaySegmentsForDatesNotMidnight(self):
      startDateTime = datetime(2011, 12, 23, 11, 23, 01)
      self.verifyDaySegmentsForDates(startDateTime, surveyLengthInDays=1,
                                     expectedNumberOfDays=2)
      self.verifyDaySegmentsForDates(startDateTime, surveyLengthInDays=2,
                                     expectedNumberOfDays=3)
      self.verifyDaySegmentsForDates(startDateTime, surveyLengthInDays=3,
                                     expectedNumberOfDays=4)

   def verifyDaysBetweenDates(self, startDateTime, surveyLengthInDays, expectedNumberOfDays):
      surveyLength = timedelta(surveyLengthInDays)
      endDateTime = startDateTime + surveyLength
      result = self.messageGenerator.getDaysBetweenDates(startDateTime, endDateTime)
      self.assertEqual(expectedNumberOfDays, result, "result should be exactly %d days, but was %d"  % (expectedNumberOfDays, result))
      
   def verifyDaySegmentsForDates(self, startDateTime, surveyLengthInDays, expectedNumberOfDays):
      surveyLength = timedelta(surveyLengthInDays)
      endDateTime = startDateTime + surveyLength
      dayStart = time(hour = 0, minute = 0, second = 0)
      dayEnd = time(hour = 23, minute = 59, second = 59)
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))
