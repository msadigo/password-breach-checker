# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Setup (once):
```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev]"
```

Run tests:
```bash
.venv/Scripts/python.exe -m pytest -q
```

Run a single test:
```bash
.venv/Scripts/python.exe -m pytest tests/test_checker.py::test_check_password_found -q
```

Run the CLI:
```bash
.venv/Scripts/python.exe -m password_breach_checker           # prompts for password securely
.venv/Scripts/python.exe -m password_breach_checker "somepw"   # or pass it as an argument
```

## Architecture

- `src/password_breach_checker/checker.py` — all breach-checking logic. `check_password(password)` implements the [HIBP Pwned Passwords k-anonymity protocol](https://haveibeenpwned.com/API/v3#PwnedPasswords): it SHA-1 hashes the password locally, sends only the first 5 hex characters to `api.pwnedpasswords.com/range/{prefix}`, and matches the remaining hash suffix against the returned list client-side. The full password and full hash never leave the machine. Raises `PwnedApiError` on network/HTTP failure.
- `src/password_breach_checker/cli.py` — argparse entry point (`main()`). Prefers `getpass.getpass()` over a positional arg so the password isn't left in shell history or visible in the process list; the positional arg exists for scripting but is documented as less secure.
- Tests mock `requests.get` directly (see `tests/test_checker.py`) rather than hitting the real API — preserve this pattern for new tests so the suite stays offline and fast.
- Packaging uses a `src/` layout with `hatchling`; the console script `password-breach-checker` is registered in `pyproject.toml` under `[project.scripts]`.
