# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Typer

from click import Context

from .. import cli

from .command_types import *

from .runs_delete import runs_delete
from .runs_list import runs_list


def runs(
    ctx: Context,
    where: RunsWhere = "",
    first: RunsFirst = 20,
):
    """Show or manage runs.

    If COMMAND is omitted, lists runs. Run 'gage runs list --help' for
    details about listing runs.
    """
    if ctx.invoked_subcommand:
        return

    from .runs_list_impl import runs_list, Args

    args = Args(
        where=where,
        first=first,
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
