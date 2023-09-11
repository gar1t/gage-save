# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Option
from typer import Typer

from .. import cli

from .check import check
from .help import help_app
from .operations import operations
from .run import run


def main(
    version: Annotated[
        bool,
        Option(
            "--version",
            help="Print program version and exit.",
            show_default=False,
        ),
    ] = False,
    cwd: Annotated[
        str,
        Option(
            "-C",
            help="Change to PATH directory for command.",
            metavar="PATH",
        ),
    ] = "",
):
    """Gage ML command line interface."""

    from .main_impl import main, Args

    main(Args(version=version, cwd=cwd))


def make_app():
    app = Typer(
        cls=cli.AliasGroup,
        rich_markup_mode="markdown",
        invoke_without_command=True,
        no_args_is_help=True,
        add_completion=False,
    )
    app.callback()(main)
    app.command()(check)
    app.add_typer(help_app())
    app.command("operations, ops")(operations)
    app.command()(run)
    return app
