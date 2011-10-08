# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import json
import subprocess
import unittest


def makeSuite(external_runner, *args):
    suite = unittest.TestSuite()
    job = subprocess.Popen(
        [external_runner, '--list'] + list(args),
        stdout=subprocess.PIPE)
    job.wait()
    output, error = job.communicate()
    result = json.loads(output)

    for testcase in result:
        suite.addTest(unittest.makeSuite(TestCase.create_from_external(
                    external_runner, testcase['case'], testcase['tests'])))
    return suite


class TestCase(unittest.TestCase):

    @classmethod
    def create_from_external(cls, external_runner, testcase, tests):
        body = dict(runner=external_runner)
        for name in tests:
            method_name = 'test_' + name.replace(' ', '_')
            method = lambda self: self._run_js_test(testcase, name)
            body[method_name] = method

        return type(
            testcase.encode('ascii') + 'JSTest',
            (cls,),
            body)

    def _run_js_test(self, testcase, testname):
        job = subprocess.Popen(
            [self.runner, '--run', testcase, testname],
            stdout=subprocess.PIPE)
        job.wait()
        output, error = job.communicate()
        result = json.loads(output)

        status = result['status']
        if status == 'SUCCESS':
            return
        elif status == 'FAIL':
            self.fail(result['message'] + result['traceback'])
        elif status == 'ERROR':
            raise RuntimeError(result['message'] + result['traceback'])
        else:
            raise ValueError(
                'JS test returned invalid test status %r' % status)
