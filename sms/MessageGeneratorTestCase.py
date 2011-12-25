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
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))
      segment = result[0]
      expectedDayStart = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedDayStart, segment.dayStart, "dayStarts should be identical: %s - %s" % (dayStart, segment.dayStart))
      expectedDayEnd = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      self.assertEqual(expectedDayEnd, segment.dayEnd, "dayEnds should be identical: %s - %s" % (dayStart, segment.dayStart))
      expectedDayLength = timedelta(days = 0, minutes = 12 * 60)
      self.assertEqual(expectedDayLength, segment.dayLength)

   def testGetDaySegmentsContentsForDatesTwoDays(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 26, 23, 59, 59)
      expectedNumberOfDays = 2
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))
      firstSegment = result[0]
      expectedDayStart = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedDayStart, firstSegment.dayStart, "dayStart should be identical: %s - %s" % (expectedDayStart, firstSegment.dayStart))
      expectedDayEnd = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      self.assertEqual(expectedDayEnd, firstSegment.dayEnd, "dayEnds should be identical: %s - %s" % (expectedDayEnd, firstSegment.dayEnd)) 
      expectedFirstDayLength = timedelta(days = 0, minutes = 12 * 60)
      self.assertEqual(expectedFirstDayLength, firstSegment.dayLength)
      lastSegment = result[1]
      expectedDayStart = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedDayStart, lastSegment.dayStart, "dayStart should be identical: %s - %s" % (expectedDayStart, lastSegment.dayStart))
      expectedDayEnd = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayEnd.hour, dayEnd.minute)
      self.assertEqual(expectedDayEnd, lastSegment.dayEnd, "dayEnds should be identical: %s - %s" % (expectedDayEnd, lastSegment.dayEnd))
      expectedLastDayLength = timedelta(days = 0, minutes = 12 * 60)
      self.assertEqual(expectedLastDayLength, lastSegment.dayLength)

   def testGetDaySegmentsContentsForDatesThreeDays(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 27, 23, 59, 59)
      expectedNumberOfDays = 3
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))
      firstSegment = result[0]
      expectedFirstDayStart = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedFirstDayStart, firstSegment.dayStart, "dayStart should be identical: %s - %s" % (expectedFirstDayStart, firstSegment.dayStart))
      expectedDayEnd = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      self.assertEqual(expectedDayEnd, firstSegment.dayEnd, "dayEnds should be identical: %s - %s" % (expectedDayEnd, firstSegment.dayEnd)) 
      expectedFirstDayLength = timedelta(days = 0, minutes = 12 * 60)
      self.assertEqual(expectedFirstDayLength, firstSegment.dayLength)
      segment2 = result[1]
      expectedDay2Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedDay2Start, segment2.dayStart, "dayStart should be identical: %s - %s" % (expectedDay2Start, segment2.dayStart))
      expectedDay2End = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayEnd.hour, dayEnd.minute)
      self.assertEqual(expectedDay2End, segment2.dayEnd, "dayEnds should be identical: %s - %s" % (expectedDay2End, segment2.dayEnd)) 
      expectedFirstDayLength = timedelta(days = 0, minutes = 12 * 60)
      self.assertEqual(expectedFirstDayLength, segment2.dayLength)
      lastSegment = result[2]
      expectedDayStart = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayStart.hour, dayStart.minute)
      self.assertEqual(expectedDayStart, lastSegment.dayStart, "dayStart should be identical: %s - %s" % (expectedDayStart, lastSegment.dayStart))
      expectedDayEnd = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayEnd.hour, dayEnd.minute)
      self.assertEqual(expectedDayEnd, lastSegment.dayEnd, "dayEnds should be identical: %s - %s" % (expectedDayEnd, lastSegment.dayEnd))
      expectedLastDayLength = timedelta(days = 0, minutes = 12 * 60)
      self.assertEqual(expectedLastDayLength, lastSegment.dayLength)


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
