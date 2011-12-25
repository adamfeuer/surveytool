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

   def testGetDaySegmentsContentsForDatesOneDay(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 25, 23, 59, 59)
      expectedNumberOfDays = 1
      result = self.getSegmentsAndVerifyCorrectNumberOfDays(expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd) 
      expectedDay1Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      expectedDay1End = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay1Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[0], expectedDay1Start, expectedDay1End, expectedDay1Length, startDateTime, endDateTime, dayStart, dayEnd)

   def testGetDaySegmentsContentsForDatesTwoDays(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 26, 23, 59, 59)
      expectedNumberOfDays = 2
      result = self.getSegmentsAndVerifyCorrectNumberOfDays(expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay1Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      expectedDay1End = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay1Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[0], expectedDay1Start, expectedDay1End, expectedDay1Length, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay2Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayStart.hour, dayStart.minute)
      expectedDay2End = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayEnd.hour, dayEnd.minute)
      expectedDay2Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[1], expectedDay2Start, expectedDay2End, expectedDay2Length, startDateTime, endDateTime, dayStart, dayEnd)

   def testGetDaySegmentsContentsForDatesThreeDays(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 27, 23, 59, 59)
      expectedNumberOfDays = 3
      result = self.getSegmentsAndVerifyCorrectNumberOfDays(expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd) 
      expectedDay1Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      expectedDay1End = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay1Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[0], expectedDay1Start, expectedDay1End, expectedDay1Length, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay2Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayStart.hour, dayStart.minute)
      expectedDay2End = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayEnd.hour, dayEnd.minute)
      expectedDay2Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[1], expectedDay2Start, expectedDay2End, expectedDay2Length, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay3Start = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayStart.hour, dayStart.minute)
      expectedDay3End = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay3Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[2], expectedDay3Start, expectedDay3End, expectedDay3Length, startDateTime, endDateTime, dayStart, dayEnd)

   def getSegmentsAndVerifyCorrectNumberOfDays(self, expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd):
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))
      return result

   def verifySegment(self, segment, expectedDayStart, expectedDayEnd, expectedDayLength, startDateTime, endDateTime, dayStart, dayEnd):
      self.assertEqual(expectedDayStart, segment.dayStart, "dayStart should be identical: %s - %s" % (expectedDayStart, segment.dayStart))
      self.assertEqual(expectedDayEnd, segment.dayEnd, "dayEnds should be identical: %s - %s" % (expectedDayEnd, segment.dayEnd))
      self.assertEqual(expectedDayLength, segment.dayLength)

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
