import hashlib
from unittest.mock import Mock, patch

import pytest
import requests

from password_breach_checker.checker import PwnedApiError, check_password


def _fake_response(text: str) -> Mock:
    response = Mock()
    response.text = text
    response.raise_for_status = Mock()
    return response


def test_check_password_found():
    password = "password123"
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    suffix = sha1[5:]
    body = f"{suffix}:42\nAAAAAAAAAAAAAAAAAAAAAAAAAAA:1"

    with patch("password_breach_checker.checker.requests.get", return_value=_fake_response(body)):
        assert check_password(password) == 42


def test_check_password_not_found():
    body = "AAAAAAAAAAAAAAAAAAAAAAAAAAA:1\nBBBBBBBBBBBBBBBBBBBBBBBBBBB:2"

    with patch("password_breach_checker.checker.requests.get", return_value=_fake_response(body)):
        assert check_password("some-unique-password") == 0


def test_check_password_api_error():
    with patch(
        "password_breach_checker.checker.requests.get",
        side_effect=requests.ConnectionError("boom"),
    ):
        with pytest.raises(PwnedApiError):
            check_password("password123")
