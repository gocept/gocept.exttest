==============
gocept.exttest
==============

Runs tests provided by an external command from Python's ``unittest.TestCase``.

.. contents:: :depth: 1


Usage
=====

gocept.exttest provides one public function, ``makeSuite``, which returns a
``unittest.TestSuite`` and takes a single argument: the name of the external
binary to run. (Any additional arguments will be passed to the external command
as command-line parameters.)

Here's a simple example::

    >>> import gocept.exttest
    ... def test_suite():
    ...     return gocept.exttest.makeSuite(
    ...         'bin/external_test_runner', '--some-arg', '--another-arg')

``makeSuite`` calls the external command to ask for a list of test cases and
test functions (see below for the exact protocol), and returns a ``TestSuite``
of ``TestCase`` objects that contain corresponding test methods. Each test
method will call the external command to run its test, and converts the results
returned by the external command to the conventions of the ``unittest`` module
(e.g. raises ``AssertionError`` for failed tests, etc.).


Requirements
============

The external command needs to understand two command line parameters:
``--list`` and ``--run <test-specification>``:

``--list`` must return a list of available test cases and test functions
formatted as JSON::

    >>> bin/external_test_runner --list
    ... [{"case": "MyExternalTestCase",
    ...   "tests": ["test_one", "test_two"]}

``--run`` is used to run one specific test, returning the results formatted as
JSON::

    >>> bin/external_test_runner --run MyExternalTestCase.test_two
    ... [{"name": "MyExternalTestCase.test_two",
    ...   "status": "FAIL",
    ...   "message": "Test failed.",
    ...   "traceback": "..."}]

NOTE: The custom JSON format for test results was chosen for simplicity when
integrating with JavaScript (see below); we'll have to evaluate whether the
commonly used XML format from `JUnitReport`_ could be used instead.

.. _`JUnitReport`: http://ant.apache.org/manual/Tasks/junitreport.html

If neither ``--list`` nor ``--run`` is given, the external command should run
all tests::

    >>> bin/external_test_runner
    ... [{"name": "MyExternalTestCase.test_one",
    ...   "status": "SUCCESS",
    ...   "message": "Test passed."},
    ...  {"name": "MyExternalTestCase.test_two",
    ...   "status": "FAIL",
    ...   "message": "Test failed.",
    ...   "traceback": "..."}]


Example: JavaScript
===================

Running tests
-------------

We built gocept.exttest to integrate javascript unittests with python
unittests. We've decided to use `Jasmine`_ as the javascript unittest
framework, running under node.js via `jasmine-node`_. (In order to use jasmine
with gocept.exttest, we extended jasmine-node to support the ``--list`` /
``-run`` arguments and the JSON output format.)

.. _`Jasmine`: http://pivotal.github.com/jasmine/
.. _`jasmine-node`: https://github.com/mhevery/jasmine-node

In your buildout environment, install node.js and jasmine-node like this::

    >>> [buildout]
    ... parts =
    ...    nodejs
    ...    test
    ...
    ... [nodejs]
    ... recipe = gp.recipe.node
    ... npms = ${buildout:directory}/../jasmine-node
    ... scripts = jasmine-node
    ...
    ... [test]
    ... recipe = zc.recipe.testrunner
    ... eggs = your.package
    ... environment = env
    ...
    ... [env]
    ... jasmine-bin = ${buildout:directory}/bin/jasmine-node

You need to checkout the jasmine-node fork from
https://github.com/wosc/jasmine-node until the changes are merged upstream. (In
the example, ``${buildout:directory}/../jasmine-node`` is used for its
location.)

Writing tests
-------------

For example, let's say the javascript tests should reside in
``your.package.tests``. `jasmine-node` supports tests written in both
JavaScript and CoffeeScript (by specifying the ``--coffee`` command-line
parameter), and requires test files to have ``_spec`` in their name.

An example test might look like this (please refer to the `Jasmine
documentation`_ for details) ::

    >>> require 'my_app.js'
    ...
    ... describe 'MyApp', ->
    ...  it 'has read Douglas Adams', ->
    ...    expect(new MyApp().calculate_the_answer()).toEqual(42)

Then wire up the tests as follows (the path to the external command is passed
to the tests via an environment variable)::

    >>> import gocept.exttest
    ... def test_suite():
    ...    return gocept.exttest.makeSuite(
    ...        os.environ.get('jasmine-bin'),
    ...        '--coffee',
    ...        '--json',
    ...        pkg_resources.resource_filename('your.package', 'tests'))


.. _`Jasmine documentation`: http://github.com/pivotal/jasmine/wiki


Development
===========

The source code is available in the mercurial repository at
https://bitbucket.org/gocept/gocept.exttest

Please report any bugs you find at
https://bitbucket.org/gocept/gocept.exttest/issues
