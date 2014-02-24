
import unittest

import StringIO

import sessionstoreparser as p

class TestHandleArgv(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeArgvHandler(object):
      def handle(self, argv):
        report.append(('handle', argv))
        return 'filename'
    mainobject = p.Main(FakeArgvHandler(), None, None, None)
    argv = ['wat']
    filename = mainobject.handleargv(argv)
    self.assertEqual(filename, 'filename')
    self.assertEqual(report, [
          ('handle', ['wat'])])

  def test_error(self):
    report = []
    class FakeArgvHandler(object):
      def handle(self, argv):
        report.append(('handle', argv))
        raise p.ArgvError('silly error')
    mainobject = p.Main(FakeArgvHandler(), None, None, None)
    argv = ['wat']
    try:
      _ = mainobject.handleargv(argv)
    except p.MainError as me:
      self.assertEqual(str(me), 'silly error')
    except Exception as e:
      self.fail('another exception expected')
    self.assertEqual(report, [
          ('handle', ['wat'])])

class TestGetSessionStore(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeJsonReader(object):
      def read(self, filename):
        report.append(('read', filename))
        return 'jsonobject'
    mainobject = p.Main(None, FakeJsonReader(), None, None)
    filename = 'filename'
    sessionstore = mainobject.getsessionstore(filename)
    self.assertEqual(sessionstore, 'jsonobject')
    self.assertEqual(report, [
          ('read', 'filename')])

class TestGetUrlGenerator(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeUrlGeneratorFactory(object):
      def produce(self):
        report.append(('produce', ))
        return 'urlgenerator'
    mainobject = p.Main(None, None, FakeUrlGeneratorFactory(), None)
    urlgenerator = mainobject.geturlgenerator()
    self.assertEqual(urlgenerator, 'urlgenerator')
    self.assertEqual(report, [
          ('produce', )])

class TestGetUrls(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeUrlGenerator(object):
      def generate(self, sessionstore):
        report.append(('generate', sessionstore))
        return 'urls'
    mainobject = p.Main(None, None, None, None)
    sessionstore = 'sessionstore'
    urls = mainobject.geturls(FakeUrlGenerator(), sessionstore)
    self.assertEqual(urls, 'urls')
    self.assertEqual(report, [
          ('generate', 'sessionstore')])

class TestWriteUrls(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeUrlWriter(object):
      def write(self, urls):
        report.append(('write', urls))
    mainobject = p.Main(None, None, None, FakeUrlWriter())
    urls = ['urls']
    mainobject.writeurls(urls)
    self.assertEqual(report, [
          ('write', ['urls'])])

class TestTryMain(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeMain(object):
      def handleargv(self, argv):
        report.append(('handleargv', argv))
        return 'filename'
      def getsessionstore(self, filename):
        report.append(('getsessionstore', filename))
        return 'sessionstore'
      def geturlgenerator(self):
        report.append(('geturlgenerator', ))
        return 'urlgenerator'
      def geturls(self, urlgenerator, sessionstore):
        report.append(('geturls', urlgenerator, sessionstore))
        return 'urls'
      def writeurls(self, urls):
        report.append(('writeurls', urls))
    fakemain = FakeMain()
    argv = ['wat']
    p.Main.trymain.__func__(fakemain, argv)
    self.assertEqual(report, [
          ('handleargv', ['wat']),
          ('getsessionstore', 'filename'),
          ('geturlgenerator', ),
          ('geturls', 'urlgenerator', 'sessionstore'),
          ('writeurls', 'urls')])

class TestMain(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeMain(object):
      def trymain(self, argv):
        report.append(('trymain', argv))
    fakemain = FakeMain()
    argv = ['wat']
    exitstatus, errormessage = p.Main.main.__func__(fakemain, argv)
    self.assertEqual(errormessage, None)
    self.assertEqual(exitstatus, 0)
    self.assertEqual(report, [
          ('trymain', ['wat'])])

  def test_error(self):
    report = []
    class FakeMain(object):
      def trymain(self, argv):
        report.append(('trymain', argv))
        raise p.MainError('silly error')
    fakemain = FakeMain()
    argv = ['wat']
    exitstatus, errormessage = p.Main.main.__func__(fakemain, argv)
    self.assertEqual(errormessage, 'silly error')
    self.assertEqual(exitstatus, 1)
    self.assertEqual(report, [
          ('trymain', ['wat'])])
