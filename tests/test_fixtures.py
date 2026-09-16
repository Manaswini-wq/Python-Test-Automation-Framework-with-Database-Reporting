import pytest
from framework.fixtures.fixture_manager import FixtureManager, FixtureScope


def test_register_and_get():
    fm = FixtureManager()
    fm.register("db", setup_fn=lambda: {"connected": True})
    val = fm.get("db")
    assert val == {"connected": True}


def test_fixture_reuse():
    call_count = 0
    def setup():
        nonlocal call_count
        call_count += 1
        return call_count

    fm = FixtureManager()
    fm.register("counter", setup_fn=setup)
    v1 = fm.get("counter")
    v2 = fm.get("counter")
    assert v1 == v2 == 1  # setup called only once


def test_teardown():
    torn_down = []
    fm = FixtureManager()
    fm.register("res", setup_fn=lambda: "resource",
                teardown_fn=lambda v: torn_down.append(v),
                scope=FixtureScope.TEST)
    fm.get("res")
    fm.teardown_scope(FixtureScope.TEST)
    assert torn_down == ["resource"]


def test_unknown_fixture():
    fm = FixtureManager()
    with pytest.raises(KeyError):
        fm.get("nonexistent")
