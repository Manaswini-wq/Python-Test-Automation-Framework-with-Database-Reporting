"""
Console reporter — prints test results to stdout with color coding.
"""
from framework.core.test_result import TestResult, SuiteResult, TestStatus


class ConsoleReporter:
    STATUS_SYMBOLS = {
        TestStatus.PASSED: "PASS",
        TestStatus.FAILED: "FAIL",
        TestStatus.ERROR: "ERR ",
        TestStatus.SKIPPED: "SKIP",
    }

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def on_suite_start(self, suite_name: str):
        print(f"\n{'='*60}")
        print(f"  Suite: {suite_name}")
        print(f"{'='*60}")

    def on_test_result(self, result: TestResult):
        symbol = self.STATUS_SYMBOLS[result.status]
        line = f"  [{symbol}] {result.test_name} ({result.duration_sec:.3f}s)"

        if result.retry_count > 0:
            line += f" [retry #{result.retry_count}]"

        print(line)

        if self.verbose and result.error_message and result.status != TestStatus.SKIPPED:
            print(f"         -> {result.error_message}")

    def on_suite_end(self, suite_result: SuiteResult):
        print(f"\n{'-'*60}")
        print(f"  Results: {suite_result.total} total | "
              f"{suite_result.passed} passed | "
              f"{suite_result.failed} failed | "
              f"{suite_result.errors} errors | "
              f"{suite_result.skipped} skipped")
        print(f"  Pass rate: {suite_result.pass_rate:.1f}%")
        print(f"  Duration:  {suite_result.duration_sec:.3f}s")
        print(f"{'='*60}\n")
