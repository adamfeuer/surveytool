#!/usr/bin/env python
import sys, os, csv

USER_ID = "Message Identifier"

class Matcher:
   """
   Takes Message Identifier CSV file from Survey Tool and Funnel results CSV
   and combines them using the message identifiers to match up each row.

   """
   def __init__(self):
      pass

   def readCsv(self, filepath):
      result = []
      reader = csv.reader(open(filepath, "rb"))
      for row in reader:
         result.append(row)
      return result

   def printCsv(self, csvList):
      for row in csvList:
         print row

   def writeCsv(self, csvList, filepath):
      writer = csv.writer(open(filepath, "wb"), dialect=csv.excel_tab)
      for row in csvList:
         writer.writerow(tuple(s.replace("\n", "") for s in row))      

   def getIdPosition(self, headerRow):
      index = 0
      for item in headerRow:
         if item == USER_ID:
            return index
         index += 1
      raise Exception('Did not find user id header.')

   def removeColumn(self, rows, columnToRemove):
      result = []
      for row in rows:
         result.append(row[0:columnToRemove] + row[columnToRemove+1:])
      return result

   def usage(self):
      print "Usage: %s [Survey Tool message identifier CSV] [Funnel results CSV] [output file]" % os.path.basename(sys.argv[0])

   def parseArgs(self):
      if len(sys.argv) != 4:
         self.usage()
         sys.exit(0)
      self.messageIdFilePath = sys.argv[1]
      self.surveyCsvFilePath = sys.argv[2]
      self.outputFilePath = sys.argv[3]
      
   def main(self):
      self.parseArgs()
      messageIdCsv = self.readCsv(self.messageIdFilePath)
      surveyCsv = self.readCsv(self.surveyCsvFilePath)
      messageIdDict = {}
      surveyDict = {}
      messageIdHeader = messageIdCsv[0]
      surveyHeader = surveyCsv[0]
      messageIdIdentifierPostiion = self.getIdPosition(messageIdHeader)
      for row in messageIdCsv[1:]:
         messageIdDict[row[messageIdIdentifierPostiion]] = row
      for row in surveyCsv[1:]:
         surveyDict[row[0]] = row
      newCsv = []
      newCsv.append(messageIdHeader + surveyHeader)
      for key in messageIdDict.keys():
         if surveyDict.has_key(key):
            newCsv.append(messageIdDict[key] + surveyDict[key])
      newCsv = self.removeColumn(newCsv, messageIdIdentifierPostiion)
      self.writeCsv(newCsv, self.outputFilePath)
      
if __name__ == "__main__":
   Matcher().main()
