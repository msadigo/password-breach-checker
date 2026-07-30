# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Initial `password-breach-checker` CLI, checking passwords against the
  Have I Been Pwned Pwned Passwords API using the k-anonymity model.
- GitHub Actions workflow running the test suite on push and pull request
  across Python 3.9-3.12.
- CI workflow status badge in README.
- MIT LICENSE.
- `requirements.txt` mirroring the runtime dependency from `pyproject.toml`.
- Expanded test coverage for `checker.py` (padding entries, empty
  responses, HTTP errors, timeouts, request assertions) and new tests for
  `cli.py` (argument handling, prompt fallback, error paths).
- "How it works" and expanded testing sections in README.
