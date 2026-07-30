import hashlib
from unittest.mock import Mock, patch

import pytest
import requests

from password_breach_checker.checker import API_URL, PwnedApiError, check_password


def _fake_response(text: str, status_ok: bool = True) -> Mock:
    response = Mock()
    response.text = text
    if status_ok:
        response.raise_for_status = Mock()
    else:
        response.raise_for_status = Mock(side_effect=requests.HTTPError("500 Server Error"))
    return response


def _hash_parts(password: str):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return sha1[:5], sha1[5:]


def test_check_password_found():
    password = "password123"
    _, suffix = _hash_parts(password)
    body = f"{suffix}:42\nAAAAAAAAAAAAAAAAAAAAAAAAAAA:1"

    with patch("password_breach_checker.checker.requests.get", return_value=_fake_response(body)):
        assert check_password(password) == 42


def test_check_password_not_found():
    body = "AAAAAAAAAAAAAAAAAAAAAAAAAAA:1\nBBBBBBBBBBBBBBBBBBBBBBBBBBB:2"

    with patch("password_breach_checker.checker.requests.get", return_value=_fake_response(body)):
        assert check_password("some-unique-password") == 0


def test_check_password_empty_response_body():
    with patch("password_breach_checker.checker.requests.get", return_value=_fake_response("")):
        assert check_password("some-unique-password") == 0


def test_check_password_ignores_padding_entries():
    # HIBP's Add-Padding feature returns dummy entries with count 0 to
    # obscure the true number of real matches; these must not be mistaken
    # for a real match.
    password = "password123"
    _, suffix = _hash_parts(password)
    body = f"AAAAAAAAAAAAAAAAAAAAAAAAAAA:0\n{suffix}:7\nBBBBBBBBBBBBBBBBBBBBBBBBBBB:0"

    with patch("password_breach_checker.checker.requests.get", return_value=_fake_response(body)):
        assert check_password(password) == 7


def test_check_password_sends_prefix_only_and_padding_header():
    password = "password123"
    prefix, _ = _hash_parts(password)

    with patch(
        "password_breach_checker.checker.requests.get", return_value=_fake_response("")
    ) as mock_get:
        check_password(password)

    mock_get.assert_called_once()
    call_args, call_kwargs = mock_get.call_args
    assert call_args[0] == API_URL.format(prefix=prefix)
    assert call_kwargs["headers"] == {"Add-Padding": "true"}
    assert "timeout" in call_kwargs


def test_check_password_connection_error():
    with patch(
        "password_breach_checker.checker.requests.get",
        side_effect=requests.ConnectionError("boom"),
    ):
        with pytest.raises(PwnedApiError):
            check_password("password123")


def test_check_password_http_error():
    with patch(
        "password_breach_checker.checker.requests.get",
        return_value=_fake_response("", status_ok=False),
    ):
        with pytest.raises(PwnedApiError):
            check_password("password123")


def test_check_password_timeout():
    with patch(
        "password_breach_checker.checker.requests.get",
        side_effect=requests.Timeout("timed out"),
    ):
        with pytest.raises(PwnedApiError):
            check_password("password123")
