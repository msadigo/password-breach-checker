import argparse
import getpass
import sys

from .checker import PwnedApiError, check_password


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="password-breach-checker",
        description="Check whether a password has appeared in known data breaches.",
    )
    parser.add_argument(
        "password",
        nargs="?",
        help=(
            "Password to check. Omit this argument to be prompted securely "
            "(recommended, avoids exposing the password in shell history/process list)."
        ),
    )
    args = parser.parse_args(argv)

    password = args.password or getpass.getpass("Password to check: ")
    if not password:
        parser.error("no password provided")

    try:
        breach_count = check_password(password)
    except PwnedApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if breach_count > 0:
        print(f"This password has been seen {breach_count:,} time(s) in known data breaches.")
        print("You should not use this password.")
    else:
        print("This password was not found in any known data breach.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
