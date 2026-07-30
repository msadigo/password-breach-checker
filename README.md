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

## Why I Built This

I previously worked as a Digitalization Support Specialist at the ECOWAS
Peace Fund (PAPS Directorate), where I was part of a team that digitized
over 20,000 institutional records across two deployments with zero
security breaches. That work made it clear that a lot of the risk to
records-handling systems doesn't come from exotic attacks — it comes from
basic credential hygiene. Weak or previously breached passwords are one of
the most common ways these systems get compromised, and checking for them
is a simple, well-understood control.

This tool also connects to my MSc research on cybersecurity framework
adoption and the security of digitized institutional records. Frameworks
routinely mandate "strong password policies," but that language says
nothing about whether the policy is actually enforced through tooling
day to day. This project is a small, concrete example of that gap: a
policy statement is not the same as a check that actually runs. It's a
modest tool, not a solution to institutional security on its own, but it's
a useful illustration of the difference between mandating a control and
operationalizing it.
