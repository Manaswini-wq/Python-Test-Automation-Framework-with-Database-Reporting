"""
Rich assertion library — readable failure messages for test cases.
"""
from typing import Any, Callable, Optional
import math


def assert_equal(actual: Any, expected: Any, msg: str = ""):
    if actual != expected:
        raise AssertionError(
            msg or f"Expected {expected!r}, got {actual!r}")


def assert_not_equal(actual: Any, expected: Any, msg: str = ""):
    if actual == expected:
        raise AssertionError(
            msg or f"Expected value different from {expected!r}")


def assert_true(condition: bool, msg: str = ""):
    if not condition:
        raise AssertionError(msg or "Expected True, got False")


def assert_false(condition: bool, msg: str = ""):
    if condition:
        raise AssertionError(msg or "Expected False, got True")


def assert_none(value: Any, msg: str = ""):
    if value is not None:
        raise AssertionError(msg or f"Expected None, got {value!r}")


def assert_not_none(value: Any, msg: str = ""):
    if value is None:
        raise AssertionError(msg or "Expected non-None value")


def assert_raises(exception_type: type, callable_fn: Callable, *args, **kwargs):
    try:
        callable_fn(*args, **kwargs)
    except exception_type:
        return
    except Exception as e:
        raise AssertionError(
            f"Expected {exception_type.__name__}, got {type(e).__name__}: {e}")
    raise AssertionError(f"Expected {exception_type.__name__} but no exception raised")


def assert_almost_equal(actual: float, expected: float, tolerance: float = 1e-6,
                        msg: str = ""):
    if math.isnan(actual) or math.isnan(expected):
        raise AssertionError(msg or f"NaN in comparison: actual={actual}, expected={expected}")
    if abs(actual - expected) > tolerance:
        raise AssertionError(
            msg or f"Expected {expected} +/- {tolerance}, got {actual} "
                   f"(diff={abs(actual - expected)})")


def assert_in(item: Any, container: Any, msg: str = ""):
    if item not in container:
        raise AssertionError(msg or f"{item!r} not found in {container!r}")


def assert_not_in(item: Any, container: Any, msg: str = ""):
    if item in container:
        raise AssertionError(msg or f"{item!r} unexpectedly found in {container!r}")


def assert_isinstance(obj: Any, expected_type: type, msg: str = ""):
    if not isinstance(obj, expected_type):
        raise AssertionError(
            msg or f"Expected instance of {expected_type.__name__}, "
                   f"got {type(obj).__name__}")


def assert_len(container: Any, expected_len: int, msg: str = ""):
    actual = len(container)
    if actual != expected_len:
        raise AssertionError(
            msg or f"Expected length {expected_len}, got {actual}")
