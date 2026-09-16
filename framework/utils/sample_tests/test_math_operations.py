"""
Sample tests — demonstrates test case writing with the framework.
"""
from framework.core.test_case import TestCase, skip, tag
from framework.assertions.matchers import (
    assert_equal, assert_almost_equal, assert_raises, assert_true
)


class TestAddition(TestCase):
    def setUp(self):
        self.calculator_ready = True

    @tag("smoke", "math")
    def test_add_positive(self):
        assert_equal(2 + 3, 5)

    @tag("math")
    def test_add_negative(self):
        assert_equal(-1 + -1, -2)

    def test_add_zero(self):
        assert_equal(0 + 0, 0)

    @tag("math")
    def test_add_float(self):
        assert_almost_equal(0.1 + 0.2, 0.3, tolerance=1e-9)


class TestDivision(TestCase):
    @tag("smoke", "math")
    def test_divide_normal(self):
        assert_equal(10 / 2, 5.0)

    def test_divide_by_zero(self):
        assert_raises(ZeroDivisionError, lambda: 1 / 0)

    @skip("Floating point edge case — investigating")
    def test_divide_precision(self):
        assert_equal(1 / 3 * 3, 1.0)

    def test_integer_division(self):
        assert_equal(7 // 2, 3)
