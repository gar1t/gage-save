# SPDX-License-Identifier: Apache-2.0

from typing import *

import json
import platform
import sys

import gage

from .. import cli
from .. import config
from .. import gagefile
from .. import project_util
from .. import util


__all__ = ["check"]

CheckData = list[tuple[str, str]]


class Args(NamedTuple):
    filename: str
    version: str
    json: bool
    verbose: bool


def check(args: Args):
    if args.filename:
        _check_gagefile_and_exit(args)
    if args.version:
        _check_version_and_exit(args)
    _print_check_info(args)


def _check_gagefile_and_exit(args: Args):
    try:
        data = gagefile.load_data(args.filename)
    except gagefile.LoadError as e:
        _handle_gagefile_load_error(e, args)
    else:
        try:
            gagefile.validate_data(data)
        except gagefile.ValidationError as e:
            _handle_gagefile_validation_error(e, args)
        else:
            cli.err(f"{args.filename} is a valid Gage file")
            raise SystemExit(0)


def _handle_gagefile_load_error(e: gagefile.LoadError, args: Args):
    cli.err(f"[red bold]ERROR[/red bold]: {args.filename}: {e}")
    raise SystemExit(1)


def _handle_gagefile_validation_error(e: gagefile.ValidationError, args: Args):
    cli.err(f"[red bold]ERROR[/red bold]: {args.filename} has problems")
    if args.verbose:
        output = gagefile.validation_error_output(e)
        cli.err(json.dumps(output, indent=2, sort_keys=True))
    else:
        for err in gagefile.validation_errors(e):
            cli.err(err)
    raise SystemExit(1)


def _check_version_and_exit(args: Args):
    try:
        match = util.check_gage_version(args.version)
    except ValueError as e:
        msg = _format_version_check_error(e)
        raise SystemExit(
            f"{msg}\nSee https://bit.ly/45AerAj for help with version specs."
        )
    else:
        if not match:
            raise SystemExit(
                f"version mismatch: current version '{gage.__version__}' "
                f"does not match '{args.version}'"
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
        ("gagefile", gagefile.filename if gagefile else "<none>"),
    ]


def _try_gagefile(cwd: str):
    try:
        return gagefile.gagefile_for_dir(cwd)
    except FileNotFoundError:
        return None


def _print_check_info_json(data: CheckData):
    cli.out(cli.json({name: val for name, val in data}))


def _print_check_info_table(data: CheckData):
    table = cli.Table()
    for name, val in data:
        table.add_row(cli.label(name), val)
    cli.out(table)
