"""
Test case base class — subclass this to write tests.
"""
from typing import Optional, Callable
import functools


class SkipTest(Exception):
    """Raise to skip a test case."""
    pass


def skip(reason: str = ""):
    """Decorator to skip a test method."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raise SkipTest(reason)
        wrapper._skip_reason = reason
        return wrapper
    return decorator


def tag(*tags: str):
    """Decorator to tag a test method for filtering."""
    def decorator(func):
        func._tags = list(tags)
        return func
    return decorator


class TestCase:
    """
    Base class for test cases. Subclass and define test_* methods.
    Provides setUp/tearDown hooks.
    """

    def setUp(self):
        """Called before each test method."""
        pass

    def tearDown(self):
        """Called after each test method (even on failure)."""
        pass

    @classmethod
    def setUpClass(cls):
        """Called once before all tests in this class."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class."""
        pass

    def get_test_methods(self) -> list[str]:
        """Return all test method names (methods starting with 'test_')."""
        return [m for m in dir(self) if m.startswith("test_") and callable(getattr(self, m))]
