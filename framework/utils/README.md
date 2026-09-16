# Test Automation Framework

A Python test automation framework with built-in test discovery, retry logic, multiple reporters (console, HTML, MongoDB), and a rich assertion library. Designed for hardware/software validation teams.

## Architecture

```
┌──────────────────┐
│  CLI / Runner     │
│  (test_runner.py) │
└────────┬─────────┘
         │
    ┌────▼─────┐    ┌──────────────┐    ┌─────────────┐
    │ Discovery │───>│  Test Suite  │───>│  Execution  │
    │ (scan dir)│    │  (classes)   │    │  (setUp/    │
    └──────────┘    └──────────────┘    │  run/tearDown)
                                        └──────┬──────┘
                                               │
              ┌────────────────────────────────┼─────────────────┐
              │                                │                 │
       ┌──────▼──────┐    ┌───────────▼──────┐  ┌──────▼──────┐
       │   Console   │    │   HTML Report    │  │   MongoDB   │
       │   Reporter  │    │   (standalone)   │  │   Reporter  │
       └─────────────┘    └──────────────────┘  └─────────────┘
```

## Quick Start

```bash
pip install -r requirements.txt

# Run sample tests
python -m framework.core.test_runner sample_tests

# Run framework's own unit tests
pytest tests/ -v
```

## Features

- **Test Discovery** — auto-finds `test_*.py` files and `TestCase` subclasses
- **setUp/tearDown** — per-test, per-class, and fixture-scoped lifecycle hooks
- **Rich Assertions** — `assert_equal`, `assert_almost_equal`, `assert_raises`, `assert_in`, etc.
- **Retry Logic** — configurable retries for flaky tests with delay
- **3 Reporters** — Console (with pass/fail summary), HTML (standalone report), MongoDB (trend analysis)
- **Flaky Test Detection** — MongoDB aggregation pipeline identifies tests that alternate pass/fail
- **Tagging** — `@tag("smoke")` decorator for test filtering
- **Skip** — `@skip("reason")` decorator

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Database | MongoDB (pymongo) |
| Templating | Jinja2-style HTML |
| Config | YAML |
| Testing | pytest (meta-tests) |
| Patterns | Observer (reporters), Strategy (discovery), Decorator (retry/skip/tag) |
