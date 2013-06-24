#! /usr/bin/env python

import json
import sys

class OpenUrlPrinter(object):

  def __init__(self):
    pass

  def doprint(self, sessionstore):
    for windows in sessionstore['windows']:
      for tab in windows['tabs']:
        openindex = tab['index'] - 1
        openentry = tab['entries'][openindex]
        openurl = openentry['url']
        sys.stdout.write(openurl + '\n')

def printopenurls(sessionstore):
  printer = OpenUrlPrinter()
  printer.doprint(sessionstore)

def main():
  if len(sys.argv) != 2:
    print 'need filename'
    sys.exit(1)
  filename = sys.argv[1]
  fileob = open(filename)
  sessionstore = json.load(fileob)
  fileob.close()
  printopenurls(sessionstore)
