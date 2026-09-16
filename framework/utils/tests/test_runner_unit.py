"""
Unit tests for the test runner itself (meta-testing).
"""
import pytest
from framework.core.test_runner import TestRunner
from framework.core.test_suite import TestSuite
from framework.core.test_case import TestCase
from framework.core.test_result import TestStatus


class PassingTest(TestCase):
    def test_pass(self):
        assert True


class FailingTest(TestCase):
    def test_fail(self):
        assert False, "Intentional failure"


class ErrorTest(TestCase):
    def test_error(self):
        raise RuntimeError("Intentional error")


class SetUpFailTest(TestCase):
    def setUp(self):
        raise RuntimeError("setUp exploded")

    def test_never_runs(self):
        pass


def make_runner():
    return TestRunner.__new__(TestRunner)


def test_passing_suite():
    runner = TestRunner(config_path="nonexistent.yaml")
    suite = TestSuite(name="PassSuite")
    suite.add_class(PassingTest)
    result = runner.run_suite(suite)
    assert result.passed == 1
    assert result.failed == 0


def test_failing_suite():
    runner = TestRunner(config_path="nonexistent.yaml")
    suite = TestSuite(name="FailSuite")
    suite.add_class(FailingTest)
    result = runner.run_suite(suite)
    assert result.failed == 1
    assert result.results[0].status == TestStatus.FAILED


def test_error_suite():
    runner = TestRunner(config_path="nonexistent.yaml")
    suite = TestSuite(name="ErrorSuite")
    suite.add_class(ErrorTest)
    result = runner.run_suite(suite)
    assert result.errors == 1
    assert result.results[0].error_message is not None


def test_setup_failure():
    runner = TestRunner(config_path="nonexistent.yaml")
    suite = TestSuite(name="SetUpFail")
    suite.add_class(SetUpFailTest)
    result = runner.run_suite(suite)
    assert result.errors == 1


def test_pass_rate():
    runner = TestRunner(config_path="nonexistent.yaml")
    suite = TestSuite(name="Mixed")
    suite.add_class(PassingTest)
    suite.add_class(FailingTest)
    result = runner.run_suite(suite)
    assert result.pass_rate == 50.0
