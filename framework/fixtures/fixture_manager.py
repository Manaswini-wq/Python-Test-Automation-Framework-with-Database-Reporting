"""
Fixture manager — provides setup/teardown resources to test cases.
Supports scoped fixtures (per-test, per-suite, per-session).
"""
from enum import Enum
from typing import Any, Callable, Optional
from dataclasses import dataclass, field


class FixtureScope(Enum):
    TEST = "test"
    SUITE = "suite"
    SESSION = "session"


@dataclass
class Fixture:
    name: str
    setup_fn: Callable[[], Any]
    teardown_fn: Optional[Callable[[Any], None]] = None
    scope: FixtureScope = FixtureScope.TEST
    _value: Any = field(default=None, repr=False)
    _initialized: bool = field(default=False, repr=False)


class FixtureManager:
    def __init__(self):
        self._fixtures: dict[str, Fixture] = {}
        self._active: dict[str, Any] = {}

    def register(self, name: str, setup_fn: Callable[[], Any],
                 teardown_fn: Optional[Callable[[Any], None]] = None,
                 scope: FixtureScope = FixtureScope.TEST):
        self._fixtures[name] = Fixture(
            name=name, setup_fn=setup_fn,
            teardown_fn=teardown_fn, scope=scope
        )

    def get(self, name: str) -> Any:
        if name not in self._fixtures:
            raise KeyError(f"Fixture '{name}' not registered")

        fixture = self._fixtures[name]

        if fixture._initialized:
            return fixture._value

        fixture._value = fixture.setup_fn()
        fixture._initialized = True
        self._active[name] = fixture
        return fixture._value

    def teardown_scope(self, scope: FixtureScope):
        to_remove = []
        for name, fixture in self._active.items():
            if fixture.scope == scope and fixture._initialized:
                if fixture.teardown_fn:
                    try:
                        fixture.teardown_fn(fixture._value)
                    except Exception:
                        pass
                fixture._initialized = False
                fixture._value = None
                to_remove.append(name)

        for name in to_remove:
            del self._active[name]

    def teardown_all(self):
        for scope in FixtureScope:
            self.teardown_scope(scope)
