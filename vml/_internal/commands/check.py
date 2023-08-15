# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

# from . import ac_support

# def _ac_all_tests(ctx, param, incomplete):
#     return (
#         _ac_builtin_tests(ctx, param, incomplete)
#         + ac_support.ac_filename(["md", "txt"], incomplete)
#     )


# def _ac_builtin_tests(ctx, _param, incomplete):
#     from .. import test
#     return [t for t in test.all_tests() if t.startswith(incomplete)]


@click.command()
@click.option("--env", help="Limit check to environment info.", is_flag=True)
# @click.option("--tensorflow", help="Check TensorFlow status.", is_flag=True)
# @click.option("--pytorch", help="Check PyTorch status.", is_flag=True)
# @click.option("--r-script", help="Check Rscript status", is_flag=True)
@click.option("-T", "--tests", "all_tests", help="Run Guild test suite.", is_flag=True)
@click.option(
    "-t",
    "--test",
    "tests",
    metavar="TEST",
    help="Run `TEST` (may be used multiple times).",
    multiple=True,
    # shell_complete=_ac_all_tests,
)
@click.option(
    "-s",
    "--skip",
    metavar="TEST",
    help="Skip `TEST` when running Guild test suite. Ignored otherwise.",
    multiple=True,
    # shell_complete=_ac_builtin_tests,
)
@click.option(
    "--force-test",
    help=(
        "Run a test even if it's skipped. Does not apply to tests "
        "specified with '--skip'."
    ),
    is_flag=True,
)
@click.option("-f", "--fast", help="Fail fast when running tests.", is_flag=True)
@click.option(
    "-c",
    "--concurrency",
    help="Number of concurrent tests.",
    type=int,
    default=None,
)
@click.option("-v", "--verbose", help="Show more information.", is_flag=True)
@click.option("--space", help="Show disk space usage for Guild files.", is_flag=True)
@click.option("-V", "--version", metavar="SPEC", help="Check the installed version.")
@click.option(
    "--notify", is_flag=True, help="Send system notification when check is complete."
)
@click.option(
    "--offline/--no-offline",
    default=None,
    help="Don't check guild.ai for latest versions.",
    is_flag=True,
)
@click.option("--check-url", hidden=True, default="http://api.guild.ai/check")
# @click.option("--uat", hidden=True, is_flag=True)
# @click.option("--force-uat", hidden=True, is_flag=True)
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
