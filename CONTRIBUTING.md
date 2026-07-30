# Contributing

## Setup

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

Run a single test:

```bash
pytest tests/test_checker.py::test_check_password_found
```

Tests mock `requests.get` directly rather than hitting the real HIBP API,
so the suite stays offline and fast — please keep new tests to this
pattern.

## Submitting changes

1. Make sure `pytest` passes locally.
2. Open a pull request. The `Tests` GitHub Actions workflow runs
   automatically on push and pull request across Python 3.9-3.12 and must
   pass before merging.
3. Update `CHANGELOG.md` under `[Unreleased]` for any user-facing change.
