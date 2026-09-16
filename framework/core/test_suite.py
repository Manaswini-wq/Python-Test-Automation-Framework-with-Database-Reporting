"""
Test suite — groups test cases and manages execution order.
"""
from framework.core.test_case import TestCase


class TestSuite:
    def __init__(self, name: str = ""):
        self.name = name
        self.test_classes: list[type[TestCase]] = []

    def add_class(self, test_class: type[TestCase]):
        if not issubclass(test_class, TestCase):
            raise TypeError(f"{test_class.__name__} must subclass TestCase")
        self.test_classes.append(test_class)

    def add_classes(self, *classes: type[TestCase]):
        for cls in classes:
            self.add_class(cls)

    def get_total_test_count(self) -> int:
        count = 0
        for cls in self.test_classes:
            instance = cls()
            count += len(instance.get_test_methods())
        return count
