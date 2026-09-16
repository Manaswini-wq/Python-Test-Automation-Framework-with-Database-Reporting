"""
Retry decorator for flaky tests or unstable operations.
"""
import functools
import time
from typing import Optional


def retry_on_failure(max_retries: int = 2, delay_sec: float = 0.1,
                     exceptions: tuple = (Exception,)):
    """Decorator that retries a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        time.sleep(delay_sec)
            raise last_exception
        return wrapper
    return decorator
