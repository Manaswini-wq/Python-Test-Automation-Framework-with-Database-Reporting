"""
Simple timer utility for measuring test execution duration.
"""
import time


class Timer:
    def __init__(self):
        self._start: float = 0
        self._end: float = 0
        self._running: bool = False

    def start(self):
        self._start = time.perf_counter()
        self._running = True

    def stop(self) -> float:
        self._end = time.perf_counter()
        self._running = False
        return self.elapsed

    @property
    def elapsed(self) -> float:
        if self._running:
            return time.perf_counter() - self._start
        return self._end - self._start
