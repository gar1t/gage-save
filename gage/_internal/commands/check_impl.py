# SPDX-License-Identifier: Apache-2.0

from typing import *

import platform
import sys

import gage

from .. import cli
from .. import util


def check(version: str):
    if version:
        _check_version_and_exit(version)
    _print_check_info()


def _check_version_and_exit(req: str):
    try:
        match = util.check_gage_version(req)
    except ValueError as e:
        raise SystemExit(
            f"{e.args[0]}\nSee https://bit.ly/45AerAj for help with version specs."
        )
    else:
        if not match:
            raise SystemExit(
                f"version mismatch: current version '{gage.__version__}' "
                f"does not match '{req}'"
            )
        else:
            raise SystemExit(0)


def _print_check_info():
    table = cli.Table(show_header=False)
    table.add_row(cli.label("gage_version"), gage.__version__)
    table.add_row(cli.label("gage_install_location"), gage.__pkgdir__)
    table.add_row(cli.label("python_version"), sys.version)
    table.add_row(cli.label("python_exe"), sys.executable)
    table.add_row(cli.label("platform"), platform.platform())
    cli.out(table)
