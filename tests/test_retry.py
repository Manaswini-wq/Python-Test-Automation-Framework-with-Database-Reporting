import pytest
from framework.utils.retry import retry_on_failure


def test_retry_succeeds_after_failures():
    attempts = []

    @retry_on_failure(max_retries=2, delay_sec=0)
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("Not ready")
        return "ok"

    result = flaky()
    assert result == "ok"
    assert len(attempts) == 3


def test_retry_exhausted():
    @retry_on_failure(max_retries=1, delay_sec=0)
    def always_fail():
        raise ValueError("Always fails")

    with pytest.raises(ValueError):
        always_fail()


def test_no_retry_on_success():
    call_count = 0

    @retry_on_failure(max_retries=3, delay_sec=0)
    def succeed():
        nonlocal call_count
        call_count += 1
        return "done"

    succeed()
    assert call_count == 1
