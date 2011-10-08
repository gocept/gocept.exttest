# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from gocept.exttest.case import makeSuite
import mock
import unittest


class FindTest(unittest.TestCase):

    @mock.patch('subprocess.Popen')
    def test_builds_test_case_classes_from_list_output(self, popen):
        popen().communicate.return_value = (
            '[{"case":"Reality","tests":["exists","fails"]}]', 0)
        combined_suite = makeSuite(
            mock.sentinel.runner, mock.sentinel.directory)
        self.assertEqual(mock.sentinel.directory, popen.call_args[0][0][2])
        self.assertEqual(2, combined_suite.countTestCases())
        suite = iter(combined_suite).next()
        suite = iter(suite)
        test = suite.next()
        self.assertEqual(
            'test_exists (gocept.exttest.case.RealityJSTest)', str(test))
        test = suite.next()
        self.assertEqual(
            'test_fails (gocept.exttest.case.RealityJSTest)', str(test))
