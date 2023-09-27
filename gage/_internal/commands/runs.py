# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Typer

from click import Context

from .. import cli

from .runs_delete import runs_delete
from .runs_list import *


def runs(
    ctx: Context,
    where: Where = "",
):
    """Show or manage runs.

    If **COMMAND** is omitted, lists runs. Run 'gage runs list --help'
    for detailed help.
    """
    if ctx.invoked_subcommand:
        return

    from .runs_list_impl import runs_list, Args

    args = Args(
        where=where,
    )
    runs_list(args)


def runs_app():
    app = Typer(
        cls=cli.AliasGroup,
        rich_markup_mode="markdown",
        invoke_without_command=True,
        add_completion=False,
    )
    app.callback()(runs)
    app.command("list")(runs_list)
    app.command("delete, rm")(runs_delete)
    return app
