from datetime import time, datetime, timedelta

from django.utils import unittest
from sms.MessageGenerator import MessageGenerator, DaySegment


class MessageGeneratorTestCase(unittest.TestCase):

   def setUp(self):
      self.messageGenerator = MessageGenerator()

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

   def testGetDaySegmentsContentsForDatesOneDayStartAfterDayStart(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 10, 1, 0)
      endDateTime = datetime(2011, 12, 25, 23, 59, 59)
      expectedNumberOfDays = 1
      result = self.getSegmentsAndVerifyCorrectNumberOfDays(expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd) 
      expectedDay1Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day, startDateTime.hour, startDateTime.minute)
      expectedDay1End = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay1Length = timedelta(days = 0, minutes = ((10 * 60) + 59))
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

   def testGetDaySegmentsContentsForDatesTwoDaysEndBeforeDayEnd(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 26, 20, 30, 00)
      expectedNumberOfDays = 2
      result = self.getSegmentsAndVerifyCorrectNumberOfDays(expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay1Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayStart.hour, dayStart.minute)
      expectedDay1End = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay1Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[0], expectedDay1Start, expectedDay1End, expectedDay1Length, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay2Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayStart.hour, dayStart.minute)
      expectedDay2End = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, endDateTime.hour, endDateTime.minute)
      expectedDay2Length = timedelta(days = 0, minutes = ((11 * 60) + 30))
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

   def testGetDaySegmentsContentsForDatesThreeDaysStartAndEndInsideWorkDay(self):
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 10, 30, 0)
      endDateTime = datetime(2011, 12, 27, 19, 30, 0)
      expectedNumberOfDays = 3
      result = self.getSegmentsAndVerifyCorrectNumberOfDays(expectedNumberOfDays, startDateTime, endDateTime, dayStart, dayEnd) 
      expectedDay1Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day, startDateTime.hour, startDateTime.minute)
      expectedDay1End = datetime(startDateTime.year, startDateTime.month, startDateTime.day, dayEnd.hour, dayEnd.minute)
      expectedDay1Length = timedelta(days = 0, minutes = 10 * 60 + 30)
      self.verifySegment(result[0], expectedDay1Start, expectedDay1End, expectedDay1Length, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay2Start = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayStart.hour, dayStart.minute)
      expectedDay2End = datetime(startDateTime.year, startDateTime.month, startDateTime.day + 1, dayEnd.hour, dayEnd.minute)
      expectedDay2Length = timedelta(days = 0, minutes = 12 * 60)
      self.verifySegment(result[1], expectedDay2Start, expectedDay2End, expectedDay2Length, startDateTime, endDateTime, dayStart, dayEnd)
      expectedDay3Start = datetime(endDateTime.year, endDateTime.month, endDateTime.day, dayStart.hour, dayStart.minute)
      expectedDay3End = datetime(endDateTime.year, endDateTime.month, endDateTime.day, endDateTime.hour, endDateTime.minute)
      expectedDay3Length = timedelta(days = 0, minutes = 10 * 60 + 30)
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

   def testGetNumberOfMessagesForSegment(self):
      messagesPerDay = 7
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 0, 0, 0)
      endDateTime = datetime(2011, 12, 25, 23, 59, 59)
      length = endDateTime - startDateTime
      segment = DaySegment(startDateTime, length, dayStart, dayEnd)
      expectedMessagesForSegment = messagesPerDay
      dayLength = datetime(2011, 12, 25, dayEnd.hour, dayEnd.minute, dayEnd.second) - datetime(2011, 12, 25, dayStart.hour, dayStart.minute, dayStart.second)
      result = self.messageGenerator.getNumberOfMessagesForSegment(segment, messagesPerDay, dayLength)
      self.assertEqual(expectedMessagesForSegment, result)

   def testGetNumberOfMessagesForSegmentPartialDay(self):
      messagesPerDay = 7
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 19, 0, 0)
      endDateTime = datetime(2011, 12, 25, 21, 0, 0)
      length = endDateTime - startDateTime
      segment = DaySegment(startDateTime, length, dayStart, dayEnd)
      segment.setDayStart(startDateTime)
      expectedMessagesForSegment = 1
      dayLength = datetime(2011, 12, 25, dayEnd.hour, dayEnd.minute, dayEnd.second) - datetime(2011, 12, 25, dayStart.hour, dayStart.minute, dayStart.second)
      result = self.messageGenerator.getNumberOfMessagesForSegment(segment, messagesPerDay, dayLength)
      self.assertEqual(expectedMessagesForSegment, result)

   def testGetMessageDateTimesForSegment(self):
      messagesPerDay = 7
      guardTimeMinutes = 15
      dayStart = time(hour = 9, minute = 0, second = 0)
      dayEnd = time(hour = 21, minute = 0, second = 0)
      startDateTime = datetime(2011, 12, 25, 9, 0, 0)
      endDateTime = datetime(2011, 12, 25, 21, 0, 0)
      length = endDateTime - startDateTime
      segment = DaySegment(startDateTime, length, dayStart, dayEnd)
      segment.setDayStart(startDateTime)
      dayLength = datetime(2011, 12, 25, dayEnd.hour, dayEnd.minute, dayEnd.second) - datetime(2011, 12, 25, dayStart.hour, dayStart.minute, dayStart.second)
      result = self.messageGenerator.getMessageDateTimesForSegment(segment, messagesPerDay, dayLength, guardTimeMinutes)
      self.assertEqual(7, len(result), "should have exactly 7 times, but was %d" % len(result) )
      self.assertTrue(result[-1].hour >= 19, "Last interval should be larger than 19.")

   def verifyDaySegmentsForDates(self, startDateTime, surveyLengthInDays, expectedNumberOfDays):
      surveyLength = timedelta(surveyLengthInDays)
      endDateTime = startDateTime + surveyLength
      dayStart = time(hour = 0, minute = 0, second = 0)
      dayEnd = time(hour = 23, minute = 59, second = 59)
      result = self.messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime, dayStart, dayEnd)
      self.assertEqual(expectedNumberOfDays, len(result), "result should contain exactly %d DaySegments, but instead contained %d [%s]"  % (expectedNumberOfDays, len(result), result))

