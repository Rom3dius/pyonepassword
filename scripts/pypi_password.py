#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser

# isort: split
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if parent_path not in sys.path:
    sys.path.append(parent_path)

from examples.do_signin import do_signin  # noqa: E402
from pyonepassword import OP  # noqa: E402
from pyonepassword.api.exceptions import (  # noqa: E402
    OPItemGetException,
    OPSigninException
)


def pypi_parse_args(args):
    parser = ArgumentParser()
    parser.add_argument(
        "--pypi-item-name", help="Optional item name for PyPI login", default="PyPI API")
    parser.add_argument("--use-session", "-S",
                        help="Attempt to use an existing 'op' session. If unsuccessful master password will be requested.", action='store_true')
    parsed = parser.parse_args(args)
    return parsed


def main():
    op: OP
    parsed = pypi_parse_args(sys.argv[1:])
    pypi_item_name = parsed.pypi_item_name
    try:
        op = do_signin(use_existing_session=parsed.use_session)
    except OPSigninException as e:
        print("sign-in failed", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)

    try:
        op_item = op.item_get(pypi_item_name)
        if hasattr(op_item, "password"):
            password = op_item.password
        else:
            password = op_item.credential
        sys.stdout.write(password)
        sys.stdout.flush()
    except OPItemGetException as e:
        print("Failed to look up password", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(1)
