# password-breach-checker

A command-line tool that checks whether a password has appeared in known
data breaches, using the [Have I Been Pwned Pwned Passwords
API](https://haveibeenpwned.com/API/v3#PwnedPasswords).

Your password never leaves your machine: only the first 5 characters of its
SHA-1 hash are sent to the API (the k-anonymity model).

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```bash
# Prompted securely (recommended)
password-breach-checker

# Or pass the password directly (visible in shell history / process list)
password-breach-checker "hunter2"
```

## Development

```bash
pytest
```
