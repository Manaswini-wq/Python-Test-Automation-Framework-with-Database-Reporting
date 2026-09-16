import pytest
from framework.discovery.test_discovery import TestDiscovery


def test_discover_sample_tests():
    discovery = TestDiscovery()
    suite = discovery.discover("sample_tests", suite_name="SampleSuite")
    assert suite.name == "SampleSuite"
    assert len(suite.test_classes) >= 3
    assert suite.get_total_test_count() >= 10


def test_discover_nonexistent_path():
    discovery = TestDiscovery()
    suite = discovery.discover("nonexistent_folder")
    assert len(suite.test_classes) == 0
