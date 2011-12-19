from django.utils import unittest
from sms.MessageGeneratorTestCase import MessageGeneratorTestCase

def suite():
   suite = unittest.TestLoader().loadTestsFromTestCase(MessageGeneratorTestCase)
   return suite
