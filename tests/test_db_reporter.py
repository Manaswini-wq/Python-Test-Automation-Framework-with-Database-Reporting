"""
Tests for DB reporter — uses mock to avoid needing a real MongoDB instance.
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from framework.reporting.db_reporter import DBReporter
from framework.core.test_result import SuiteResult, TestResult, TestStatus


def make_suite_result():
    sr = SuiteResult(suite_name="TestSuite")
    sr.start_time = datetime.now(timezone.utc)
    sr.end_time = datetime.now(timezone.utc)
    sr.results.append(TestResult(
        test_name="TestClass.test_one",
        suite_name="TestSuite",
        status=TestStatus.PASSED,
        duration_sec=0.05,
    ))
    sr.results.append(TestResult(
        test_name="TestClass.test_two",
        suite_name="TestSuite",
        status=TestStatus.FAILED,
        duration_sec=0.12,
        error_message="assertion failed",
    ))
    return sr


@patch("framework.reporting.db_reporter.MongoClient")
def test_stores_results(mock_mongo_cls):
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.__getitem__ = MagicMock(return_value={})
    mock_mongo_cls.return_value = mock_client
    mock_client.__getitem__.return_value.__getitem__ = MagicMock(return_value=mock_collection)

    reporter = DBReporter()
    sr = make_suite_result()
    reporter.on_suite_end(sr)

    mock_collection.insert_one.assert_called_once()
    doc = mock_collection.insert_one.call_args[0][0]
    assert doc["suite_name"] == "TestSuite"
    assert doc["total"] == 2
    assert doc["passed"] == 1
    assert doc["failed"] == 1
