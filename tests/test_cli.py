from unittest.mock import patch

import pytest

from password_breach_checker.checker import PwnedApiError
from password_breach_checker.cli import main


def test_main_password_arg_not_breached(capsys):
    with patch("password_breach_checker.cli.check_password", return_value=0):
        exit_code = main(["some-unique-password"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "not found in any known data breach" in out


def test_main_password_arg_breached(capsys):
    with patch("password_breach_checker.cli.check_password", return_value=42):
        exit_code = main(["password123"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "42" in out
    assert "should not use this password" in out


def test_main_prompts_when_no_password_arg(capsys):
    with patch("password_breach_checker.cli.getpass.getpass", return_value="prompted-pw") as mock_getpass, \
         patch("password_breach_checker.cli.check_password", return_value=0) as mock_check:
        exit_code = main([])

    assert exit_code == 0
    mock_getpass.assert_called_once()
    mock_check.assert_called_once_with("prompted-pw")


def test_main_empty_password_is_an_error():
    with patch("password_breach_checker.cli.getpass.getpass", return_value=""):
        with pytest.raises(SystemExit) as exc_info:
            main([])

    assert exc_info.value.code == 2


def test_main_api_error_prints_to_stderr_and_returns_1(capsys):
    with patch(
        "password_breach_checker.cli.check_password",
        side_effect=PwnedApiError("network down"),
    ):
        exit_code = main(["password123"])

    assert exit_code == 1
    err = capsys.readouterr().err
    assert "network down" in err
