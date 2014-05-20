
import unittest

import StringIO

import sessionstoreparser as p

class TestHandleArgv(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeArgvHandler(object):
      def handle(self, argv):
        report.append(('handle', argv))
        return 'options'
    app = p.Application(FakeArgvHandler(), None, None, None)
    options = app.handleargv(['progname', 'argv'])
    self.assertEqual(options, 'options')
    self.assertEqual(report, [
          ('handle', ['argv'])])

class TestTryRun(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeApplication(object):
      def handleargv(self, argv):
        report.append(('handleargv', argv))
        return 'options'
      def getsessionstore(self, options):
        report.append(('getsessionstore', options))
        return 'sessionstore'
      def geturlgenerator(self):
        report.append(('geturlgenerator', ))
        return 'urlgenerator'
      def geturls(self, urlgenerator, sessionstore):
        report.append(('geturls', urlgenerator, sessionstore))
        return 'urls'
      def writeurls(self, urls):
        report.append(('writeurls', urls))
    fakeapp = FakeApplication()
    p.Application.tryrun.__func__(fakeapp, 'argv')
    self.assertEqual(report, [
          ('handleargv', 'argv'),
          ('getsessionstore', 'options'),
          ('geturlgenerator', ),
          ('geturls', 'urlgenerator', 'sessionstore'),
          ('writeurls', 'urls')])

class TestRun(unittest.TestCase):

  def test_noerror(self):
    report = []
    class FakeApplication(object):
      def tryrun(self, argv):
        report.append(('tryrun', argv))
    fakeapp = FakeApplication()
    stderr = StringIO.StringIO()
    exitstatus = p.Application.run.__func__(fakeapp, 'argv', stderr)
    self.assertEqual(stderr.getvalue(), '')
    self.assertEqual(exitstatus, 0)
    self.assertEqual(report, [
          ('tryrun', 'argv')])

  def test_argverror(self):
    report = []
    class FakeApplication(object):
      def tryrun(self, argv):
        report.append(('tryrun', argv))
        raise p.ArgvError('argv error')
    fakeapp = FakeApplication()
    stderr = StringIO.StringIO()
    exitstatus = p.Application.run.__func__(fakeapp, 'argv', stderr)
    self.assertEqual(stderr.getvalue(), 'argv error\n')
    self.assertEqual(exitstatus, 2)
    self.assertEqual(report, [
          ('tryrun', 'argv')])

  def test_genericerror(self):
    report = []
    class FakeApplication(object):
      def tryrun(self, argv):
        report.append(('tryrun', argv))
        raise p.Error('generic error')
    fakeapp = FakeApplication()
    stderr = StringIO.StringIO()
    exitstatus = p.Application.run.__func__(fakeapp, 'argv', stderr)
    self.assertEqual(stderr.getvalue(), 'generic error\n')
    self.assertEqual(exitstatus, 1)
    self.assertEqual(report, [
          ('tryrun', 'argv')])