from framework.core.test_case import TestCase, tag
from framework.assertions.matchers import (
    assert_equal, assert_true, assert_in, assert_len, assert_isinstance
)


class TestStringOperations(TestCase):
    def setUp(self):
        self.sample = "Hello, World!"

    @tag("smoke")
    def test_upper(self):
        assert_equal(self.sample.upper(), "HELLO, WORLD!")

    def test_lower(self):
        assert_equal(self.sample.lower(), "hello, world!")

    def test_split(self):
        parts = self.sample.split(", ")
        assert_len(parts, 2)
        assert_equal(parts[0], "Hello")

    def test_contains(self):
        assert_in("World", self.sample)

    def test_strip(self):
        assert_equal("  hello  ".strip(), "hello")

    def test_replace(self):
        result = self.sample.replace("World", "Python")
        assert_equal(result, "Hello, Python!")

    def test_type(self):
        assert_isinstance(self.sample, str)
