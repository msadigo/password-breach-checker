"""Check passwords against the Have I Been Pwned Pwned Passwords API.

Uses the k-anonymity model: only the first 5 characters of the SHA-1 hash
of the password are sent to the API. The full password never leaves the
machine.
"""

import hashlib

import requests

API_URL = "https://api.pwnedpasswords.com/range/{prefix}"
REQUEST_TIMEOUT_SECONDS = 10


class PwnedApiError(Exception):
    """Raised when the Pwned Passwords API cannot be reached or errors out."""


def check_password(password: str) -> int:
    """Return the number of times `password` has appeared in known breaches.

    Returns 0 if the password was not found in any breach.
    Raises PwnedApiError if the API request fails.
    """
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    try:
        response = requests.get(
            API_URL.format(prefix=prefix),
            timeout=REQUEST_TIMEOUT_SECONDS,
            headers={"Add-Padding": "true"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise PwnedApiError(f"Failed to reach Pwned Passwords API: {exc}") from exc

    for line in response.text.splitlines():
        hash_suffix, _, count = line.partition(":")
        if hash_suffix == suffix:
            return int(count)

    return 0
