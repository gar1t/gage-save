# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Option
from typer import Typer

from .. import cli

from .check import check
from .help import help_app
from .open import open
from .operations import operations
from .run import run
from .runs_list import runs_list
from .select import select
from .show import show

VersionFlag = Annotated[
    bool,
    Option(
        "--version",
        help="Print program version and exit.",
        show_default=False,
    ),
]

Cwd = Annotated[
    str,
    Option(
        "-C",
        metavar="path",
        help="Change directory for command.",
    ),
]


def main(
    version: VersionFlag = False,
    cwd: Cwd = "",
):
    """Gage ML command line interface."""

    from .main_impl import main, Args

    main(Args(version=version, cwd=cwd))


def main_app():
    app = Typer(
        cls=cli.AliasGroup,
        rich_markup_mode="rich",
        invoke_without_command=True,
        no_args_is_help=True,
        add_completion=False,
        pretty_exceptions_enable=not cli.is_plain,
        pretty_exceptions_show_locals=False,
        context_settings={
            "help_option_names": ("-h", "--help"),
        },
        subcommand_metavar="command",
        options_metavar="[options]",
    )
    app.callback()(main)
    app.command("check")(check)
    app.add_typer(help_app())
    app.command("open")(open)
    app.command("operations, ops")(operations)
    app.command("run")(run)
    app.command("list, ls")(runs_list)
    app.command("select")(select)
    app.command("show")(show)
    return app
