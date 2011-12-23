from datetime import time, datetime, timedelta

from django.utils import unittest
from sms.MessageGenerator import MessageGenerator, DaySegment


class MessageGeneratorTestCase(unittest.TestCase):

   def setUp(self):
      self.messageGenerator = MessageGenerator()

   def test_nothing(self):
      self.assertEqual(True, True, "True is not equal to True!")

   def testGetDaySegments(self):
      startDateTime = datetime.now()
      threeDays = 3
      surveyLength = timedelta(threeDays)
      endDateTime = startDateTime + surveyLength
      messageGenerator = MessageGenerator()
      result = messageGenerator.getDaySegments(startDateTime, endDateTime)
      self.assertIsNotNone(result, "result should not return None!")
      self.assertEqual(3, len(result), "result should contain exactly 3 segments!")
      self.assertEqual(startDateTime, result[0].start, "result[0] should have a start.")

   def testGetDaysBetweenDates(self):
      startDateTime = datetime.now()
      surveyLengthInDays = 1
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays)
      surveyLengthInDays = 2
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays)
      surveyLengthInDays = 3
      self.verifyDaysBetweenDates(startDateTime, surveyLengthInDays)

   def verifyDaysBetweenDates(self, startDateTime, surveyLengthInDays):
      surveyLength = timedelta(surveyLengthInDays)
      endDateTime = startDateTime + surveyLength
      result = self.messageGenerator.getDaysBetweenDates(startDateTime, endDateTime)
      self.assertEqual (surveyLengthInDays, result, "result should be exactly %d days, but was %d"  % (surveyLengthInDays, result))
      
      
      
