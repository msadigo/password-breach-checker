# password-breach-checker

[![Tests](https://github.com/msadigo/password-breach-checker/actions/workflows/tests.yml/badge.svg)](https://github.com/msadigo/password-breach-checker/actions/workflows/tests.yml)

A command-line tool that checks whether a password has appeared in known
data breaches, using the [Have I Been Pwned Pwned Passwords
API](https://haveibeenpwned.com/API/v3#PwnedPasswords).

Your password never leaves your machine: only the first 5 characters of its
SHA-1 hash are sent to the API (the k-anonymity model).

## How it works

1. The password is hashed locally with SHA-1.
2. Only the first 5 characters of the hash (the "prefix") are sent to the
   HIBP Pwned Passwords API.
3. The API returns every hash suffix in that prefix bucket, along with how
   many times each one has been seen in a breach.
4. The remaining 35 characters of the local hash (the "suffix") are matched
   against that list locally to get the breach count.

Because the full hash is never transmitted, the API operator cannot
determine which password was checked.

## Install

```bash
pip install -e ".[dev]"
```

Or, for a runtime-only install without the test dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Prompted securely (recommended)
password-breach-checker

# Or pass the password directly (visible in shell history / process list)
password-breach-checker "hunter2"
```

## Development

Run the full test suite:

```bash
pytest
```

Run a single test:

```bash
pytest tests/test_checker.py::test_check_password_found
```

Tests mock `requests.get` directly, so they run offline and never hit the
real HIBP API.
