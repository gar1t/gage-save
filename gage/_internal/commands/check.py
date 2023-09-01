# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util


@click.command()
@click.option("-v", "--verbose", help="Show more information.", is_flag=True)
@click.option("--space", help="Show disk space usage for Guild files.", is_flag=True)
@click.option("--version", metavar="SPEC", help="Check the installed version.")
@click.option(
    "--offline/--no-offline",
    default=None,
    help="Don't check guild.ai for latest versions.",
    is_flag=True,
)
@click.option("--external", hidden=True)
@click.option("--no-chrome", hidden=True, is_flag=True)
@click_util.use_args
@click_util.render_doc
def check(args: Any):
    """Check the Guild setup.

    This command performs a number of checks and prints information
    about the Guild installation.

    Run the Guild test suite by specifying the `--tests` option.

    Run a test file using `--test FILE`. Test files must be valid
    doctest files. See https://docs.python.org/library/doctest.html
    for details.

    To verify that the installed version of Guild matches a required
    spec, use `--version`. REQUIRED can be any valid version
    requirement. For example, to confirm that Guild is at least
    version 0.7.0, use `--version '>=0.7.0'`. Note you must quote
    arguments that contain less-than or greater-than symbols in POSIX
    shells.
    """
    from . import check_impl

    check_impl.main(args)
