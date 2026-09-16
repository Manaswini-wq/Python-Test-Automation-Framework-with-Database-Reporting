"""
Test runner — orchestrates test execution, fixture management, and reporting.
"""
import sys
import traceback
import yaml
from datetime import datetime, timezone
from typing import Optional

from framework.core.test_suite import TestSuite
from framework.core.test_case import TestCase, SkipTest
from framework.core.test_result import TestResult, SuiteResult, TestStatus
from framework.fixtures.fixture_manager import FixtureManager
from framework.reporting.console_reporter import ConsoleReporter
from framework.reporting.db_reporter import DBReporter
from framework.reporting.html_reporter import HTMLReporter
from framework.utils.retry import retry_on_failure
from framework.utils.timer import Timer


class TestRunner:
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        self.fixture_manager = FixtureManager()
        self.reporters = []
        self._setup_reporters()

    def _load_config(self, path: str) -> dict:
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {
                "runner": {"max_retries": 0, "verbose": True, "timeout_sec": 30},
                "reporting": {"console": True, "html": False, "database": False},
            }

    def _setup_reporters(self):
        rpt = self.config.get("reporting", {})
        if rpt.get("console", True):
            self.reporters.append(ConsoleReporter(
                verbose=self.config.get("runner", {}).get("verbose", True)))
        if rpt.get("html", False):
            self.reporters.append(HTMLReporter(
                output_path=rpt.get("html_output", "reports/test_report.html")))
        if rpt.get("database", False):
            db_cfg = self.config.get("database", {})
            self.reporters.append(DBReporter(
                uri=db_cfg.get("uri", "mongodb://localhost:27017"),
                db_name=db_cfg.get("name", "test_results"),
                collection=db_cfg.get("collection", "runs"),
            ))

    def run_suite(self, suite: TestSuite) -> SuiteResult:
        suite_result = SuiteResult(
            suite_name=suite.name,
            start_time=datetime.now(timezone.utc),
        )

        for reporter in self.reporters:
            reporter.on_suite_start(suite.name)

        for test_class in suite.test_classes:
            self._run_test_class(test_class, suite_result)

        suite_result.end_time = datetime.now(timezone.utc)

        for reporter in self.reporters:
            reporter.on_suite_end(suite_result)

        return suite_result

    def _run_test_class(self, test_class: type[TestCase], suite_result: SuiteResult):
        instance = test_class()
        max_retries = self.config.get("runner", {}).get("max_retries", 0)

        try:
            test_class.setUpClass()
        except Exception as e:
            for method_name in instance.get_test_methods():
                result = TestResult(
                    test_name=f"{test_class.__name__}.{method_name}",
                    suite_name=suite_result.suite_name,
                    status=TestStatus.ERROR,
                    duration_sec=0,
                    error_message=f"setUpClass failed: {e}",
                    error_traceback=traceback.format_exc(),
                )
                suite_result.results.append(result)
            return

        for method_name in instance.get_test_methods():
            method = getattr(instance, method_name)
            tags = getattr(method, "_tags", [])
            result = self._run_single_test(instance, method_name, suite_result.suite_name,
                                           max_retries, tags)
            suite_result.results.append(result)

            for reporter in self.reporters:
                reporter.on_test_result(result)

        try:
            test_class.tearDownClass()
        except Exception:
            pass

    def _run_single_test(self, instance: TestCase, method_name: str,
                         suite_name: str, max_retries: int,
                         tags: list[str]) -> TestResult:
        full_name = f"{instance.__class__.__name__}.{method_name}"
        last_result = None

        for attempt in range(max_retries + 1):
            timer = Timer()
            timer.start()
            status = TestStatus.PASSED
            error_msg = None
            error_tb = None

            try:
                instance.setUp()
                getattr(instance, method_name)()
            except SkipTest as e:
                status = TestStatus.SKIPPED
                error_msg = str(e)
            except AssertionError as e:
                status = TestStatus.FAILED
                error_msg = str(e)
                error_tb = traceback.format_exc()
            except Exception as e:
                status = TestStatus.ERROR
                error_msg = f"{type(e).__name__}: {e}"
                error_tb = traceback.format_exc()
            finally:
                try:
                    instance.tearDown()
                except Exception:
                    pass
                timer.stop()

            last_result = TestResult(
                test_name=full_name,
                suite_name=suite_name,
                status=status,
                duration_sec=timer.elapsed,
                error_message=error_msg,
                error_traceback=error_tb,
                retry_count=attempt,
                tags=tags,
            )

            if status in (TestStatus.PASSED, TestStatus.SKIPPED):
                break

        return last_result


def main():
    """CLI entry point — discovers and runs tests."""
    from framework.discovery.test_discovery import TestDiscovery

    search_path = sys.argv[1] if len(sys.argv) > 1 else "sample_tests"
    config_path = sys.argv[2] if len(sys.argv) > 2 else "config/settings.yaml"

    discovery = TestDiscovery()
    suite = discovery.discover(search_path, suite_name="Discovered Tests")

    runner = TestRunner(config_path=config_path)
    result = runner.run_suite(suite)

    sys.exit(0 if result.failed + result.errors == 0 else 1)


if __name__ == "__main__":
    main()
