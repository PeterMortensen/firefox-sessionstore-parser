#! /usr/bin/env python

import json

class WindowsGenerator(object):
  def __init__(self):
    pass

  def generate(self, sessionstore):
    for windows in sessionstore['windows']:
      yield windows

class TabGenerator(object):
  def __init__(self, windowsgenerator):
    self.windowsgenerator = windowsgenerator

  def generate(self, sessionstore):
    for windows in self.windowsgenerator.generate(sessionstore):
      for tab in windows['tabs']:
        yield tab

class OpenUrlGenerator(object):
  def __init__(self, tabgenerator):
    self.tabgenerator = tabgenerator

  def generate(self, sessionstore):
    for tab in self.tabgenerator.generate(sessionstore):
      openindex = tab['index'] - 1
      openentry = tab['entries'][openindex]
      openurl = openentry['url']
      yield openurl

class ArgvError(Exception):
  pass

class ArgvHandler(object):
  def __init__(self):
    pass

  def handle(self, argv):
    if len(argv) != 2:
      success = False
      filename = None
      errormessage = 'need filename'
    else:
      success = True
      filename = argv[1]
      errormessage = None
    if not success:
      raise ArgvError(errormessage)
    return filename

class JsonReader(object):
  def __init__(self, openfunc):
    self.openfunc = openfunc

  def read(self, filename):
    with self.openfunc(filename) as fileob:
      sessionstore = json.load(fileob)
    return sessionstore

class ParserFactory(object):
  def __init__(self):
    pass

  def produce(self):
    windowsgenerator = WindowsGenerator()
    tabgenerator = TabGenerator(windowsgenerator)
    urlgenerator = OpenUrlGenerator(tabgenerator)
    return urlgenerator

class UrlWriter(object):
  def __init__(self, stdout):
    self.stdout = stdout

  def write(self, urls):
    for url in urls:
      self.stdout.write(url + '\n')

class MainError(Exception):
  pass

class Main(object):

  def __init__(self, stdout, openfunc):
    self.argvhandler = ArgvHandler()
    self.jsonreader = JsonReader(openfunc)
    self.parserfactory = ParserFactory()
    self.urlwriter = UrlWriter(stdout)

  def handleargv(self, argv):
    try:
      filename = self.argvhandler.handle(argv)
      return filename
    except ArgvError as ae:
      errormessage = str(ae)
      raise MainError(errormessage)

  def getsessionstore(self, filename):
    sessionstore = self.jsonreader.read(filename)
    return sessionstore

  def getparser(self):
    parser = self.parserfactory.produce()
    return parser

  def geturls(self, parser, sessionstore):
    urls = parser.generate(sessionstore)
    return urls

  def writeurls(self, urls):
    self.urlwriter.write(urls)

  def trymain(self, argv):
    filename = self.handleargv(argv)
    sessionstore = self.getsessionstore(filename)
    parser = self.getparser()
    urls = self.geturls(parser, sessionstore)
    self.writeurls(urls)

  def main(self, argv):
    try:
      self.trymain(argv)
      return 0, None
    except MainError as me:
      return 1, str(me)

def main():
  import sys
  main = Main(sys.stdout, open)
  exitstatus, errormessage = main.main(sys.argv)
  if errormessage is not None:
    sys.stderr.write(errormessage + '\n')
  return exitstatus
