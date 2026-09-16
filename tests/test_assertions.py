import pytest
from framework.assertions.matchers import (
    assert_equal, assert_not_equal, assert_true, assert_false,
    assert_none, assert_not_none, assert_raises, assert_almost_equal,
    assert_in, assert_not_in, assert_isinstance, assert_len
)


def test_assert_equal_pass():
    assert_equal(1, 1)
    assert_equal("abc", "abc")


def test_assert_equal_fail():
    with pytest.raises(AssertionError):
        assert_equal(1, 2)


def test_assert_not_equal():
    assert_not_equal(1, 2)
    with pytest.raises(AssertionError):
        assert_not_equal(1, 1)


def test_assert_true_false():
    assert_true(True)
    assert_false(False)
    with pytest.raises(AssertionError):
        assert_true(False)


def test_assert_none():
    assert_none(None)
    assert_not_none(42)
    with pytest.raises(AssertionError):
        assert_none(42)


def test_assert_raises():
    assert_raises(ValueError, int, "not_a_number")
    with pytest.raises(AssertionError):
        assert_raises(ValueError, int, "42")  # no exception


def test_assert_almost_equal():
    assert_almost_equal(0.1 + 0.2, 0.3, tolerance=1e-9)
    with pytest.raises(AssertionError):
        assert_almost_equal(1.0, 2.0, tolerance=0.1)


def test_assert_in():
    assert_in(3, [1, 2, 3])
    with pytest.raises(AssertionError):
        assert_in(4, [1, 2, 3])


def test_assert_isinstance():
    assert_isinstance("hello", str)
    with pytest.raises(AssertionError):
        assert_isinstance("hello", int)


def test_assert_len():
    assert_len([1, 2, 3], 3)
    with pytest.raises(AssertionError):
        assert_len([1, 2], 3)
