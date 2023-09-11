# SPDX-License-Identifier: Apache-2.0

from typing import *

import platform
import sys

import gage

from .. import cli
from .. import gagefile
from .. import config
from .. import project_util
from .. import util

__all__ = ["check"]

CheckData = list[tuple[str, str]]


class Args(NamedTuple):
    version: str
    json: bool
    verbose: bool


def check(args: Args):
    if args.version:
        _check_version_and_exit(args.version)
    _print_check_info(args)


def _check_version_and_exit(req: str):
    try:
        match = util.check_gage_version(req)
    except ValueError as e:
        msg = _format_version_check_error(e)
        raise SystemExit(
            f"{msg}\nSee https://bit.ly/45AerAj for help with version specs."
        )
    else:
        if not match:
            raise SystemExit(
                f"version mismatch: current version '{gage.__version__}' "
                f"does not match '{req}'"
            )
        else:
            raise SystemExit(0)


def _format_version_check_error(e: ValueError):
    return e.args[0].split("\n")[0].lower()


def _print_check_info(args: Args):
    data = _check_info_data(args)
    if args.json:
        _print_check_info_json(data)
    else:
        _print_check_info_table(data)


def _check_info_data(args: Args):
    return _core_info_data() + _maybe_verbose_info_data(args.verbose)


def _core_info_data() -> CheckData:
    return [
        ("gage_version", gage.__version__),
        ("gage_install_location", gage.__pkgdir__),
        ("python_version", sys.version),
        ("python_exe", sys.executable),
        ("platform", platform.platform()),
    ]


def _maybe_verbose_info_data(verbose: bool) -> CheckData:
    if not verbose:
        return []
    cwd = config.cwd()
    project_dir = project_util.find_project(cwd)
    gagefile = _try_gagefile(cwd)
    return [
        ("command_directory", cwd),
        ("project_directory", project_dir or "<none>"),
        ("gagefile", gagefile.filename if gagefile  else "<none>"),
    ]

def _try_gagefile(cwd: str):
    try:
        return gagefile.for_dir(cwd)
    except FileNotFoundError:
        return None


def _print_check_info_json(data: CheckData):
    cli.out(cli.json({name: val for name, val in data}))


def _print_check_info_table(data: CheckData):
    table = cli.Table(show_header=False)
    for name, val in data:
        table.add_row(cli.label(name), val)
    cli.out(table)
