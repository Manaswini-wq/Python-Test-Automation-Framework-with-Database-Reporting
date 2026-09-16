"""
Test result data model — stores outcome, duration, error info for each test case.
"""
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


class TestStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


@dataclass
class TestResult:
    test_name: str
    suite_name: str
    status: TestStatus
    duration_sec: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    retry_count: int = 0
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "suite_name": self.suite_name,
            "status": self.status.value,
            "duration_sec": round(self.duration_sec, 4),
            "timestamp": self.timestamp,
            "error_message": self.error_message,
            "error_traceback": self.error_traceback,
            "retry_count": self.retry_count,
            "tags": self.tags,
        }

    @property
    def passed(self) -> bool:
        return self.status == TestStatus.PASSED


@dataclass
class SuiteResult:
    suite_name: str
    results: list[TestResult] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.PASSED)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.FAILED)

    @property
    def errors(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.ERROR)

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.SKIPPED)

    @property
    def duration_sec(self) -> float:
        return sum(r.duration_sec for r in self.results)

    @property
    def pass_rate(self) -> float:
        return (self.passed / self.total * 100) if self.total > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            "suite_name": self.suite_name,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "skipped": self.skipped,
            "pass_rate": round(self.pass_rate, 1),
            "duration_sec": round(self.duration_sec, 4),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "results": [r.to_dict() for r in self.results],
        }
