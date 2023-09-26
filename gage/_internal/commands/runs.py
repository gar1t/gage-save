# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Typer

from .runs_list import runs_list


HELP = """
Show or manage runs.

If COMMAND is omitted, lists runs. Run 'gage runs list --help' for
details about listing runs.
"""


def runs_app():
    app = Typer(
        rich_markup_mode="markdown",
        invoke_without_command=True,
        add_completion=False,
    )
    app.callback(name="runs", help=HELP)(runs_list)
    app.command(name="list")(runs_list)
    return app
