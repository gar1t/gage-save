# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Option
from typer import Typer

from .. import cli

from .associate import associate
from .check import check
from .comment import comment
from .help import help_app
from .label import label
from .open import open
from .operations import operations
from .run import run
from .runs_delete import runs_delete
from .runs_list import runs_list
from .runs_purge import runs_purge
from .runs_restore import runs_restore
from .select import select
from .show import show

VersionFlag = Annotated[
    bool,
    Option(
        "--version",
        help="Print program version and exit.",
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

DebugFlag = Annotated[
    bool,
    Option(
        "--debug",
        help="Show debug messages.",
    ),
]


def main(
    version: VersionFlag = False,
    cwd: Cwd = "",
    debug: DebugFlag = False,
):
    """Gage ML command line interface."""

    from .main_impl import main, Args

    main(Args(version, cwd, debug))


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
    app.command("associate")(associate)
    app.command("check")(check)
    app.command("comment")(comment)
    app.command("delete, rm")(runs_delete)
    app.add_typer(help_app())
    app.command("label")(label)
    app.command("list, ls")(runs_list)
    app.command("open")(open)
    app.command("operations, ops")(operations)
    app.command("purge")(runs_purge)
    app.command("restore")(runs_restore)
    app.command("run")(run)
    app.command("select")(select)
    app.command("show")(show)
    return app
