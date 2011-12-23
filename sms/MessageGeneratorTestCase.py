from datetime import time, datetime, timedelta

from django.utils import unittest
from sms.MessageGenerator import MessageGenerator, DaySegment


class MessageGeneratorTestCase(unittest.TestCase):

   def setUp(self):
      self.messageGenerator = MessageGenerator()

   def test_nothing(self):
      self.assertEqual(True, True, "True is not equal to True!")

   def testGetDaySegmentsForDates(self):
      startDateTime = datetime.now()
      threeDays = 3
      surveyLength = timedelta(threeDays)
      endDateTime = startDateTime + surveyLength
      messageGenerator = MessageGenerator()
      result = messageGenerator.getDaySegmentsForDates(startDateTime, endDateTime)
      self.assertIsNotNone(result, "result should not return None!")
      self.assertEqual(4, len(result), "result should contain exactly 4 segments but was %s" % result)

   def testGetDaysBetweenDatesStartMidnight(self):
      startDateTime = datetime(2011, 12, 23, 0, 0, 0)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=1, expectedResult=1)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=2, expectedResult=2)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=3, expectedResult=3)

   def testGetDaysBetweenDatesStartNotMidnight(self):
      startDateTime = datetime(2011, 12, 23, 9, 30, 0)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=1, expectedResult=2)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=2, expectedResult=3)
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays=3, expectedResult=4)

   def verifyDaysBetweenDates(self, startDateTime, surveyLengthInDays, expectedResult):
      surveyLength = timedelta(surveyLengthInDays)
      endDateTime = startDateTime + surveyLength
      result = self.messageGenerator.getDaysBetweenDates(startDateTime, endDateTime)
      self.assertEqual(expectedResult, result, "result should be exactly %d days, but was %d"  % (expectedResult, result))
      
      
      
