# Security Policy

## Supported Versions

This project is pre-1.0 and does not yet maintain separate maintenance
branches. Security fixes are applied to the latest commit on `master`.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately by
emailing adigoyakubuattah@gmail.com rather than opening a public issue.
Include as much detail as possible (steps to reproduce, affected version/
commit, potential impact) so it can be triaged quickly.

You should receive an acknowledgment within a few days. Once a fix is
available, it will be released and the reporter credited, unless
anonymity is requested.

## Design Notes Relevant to Security

- Passwords are never logged, stored, or transmitted in full. Only the
  first 5 characters of a password's SHA-1 hash are sent to the Have I
  Been Pwned Pwned Passwords API (the k-anonymity model) — see
  [README.md](README.md#how-it-works) for details.
- The CLI prefers a hidden prompt (`getpass`) over a command-line argument
  to avoid exposing passwords in shell history or the process list.
