# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

import typer
from typer import Option

from .__init__ import __version__

from ._internal import cli
from ._internal import exitcodes

from ._internal.commands.check import check
from ._internal.commands.run import run


if os.getenv("TERM") in ("unknown", "dumb"):
    import typer.core

    # Disable use of Rich formatting
    typer.core.rich = None  # type: ignore


def main():
    app = typer.Typer(
        rich_markup_mode="markdown",
        invoke_without_command=True,
        no_args_is_help=True,
        add_completion=False,
    )
    app.callback()(_main)
    app.command()(check)
    app.command()(run)

    try:
        app()
    except SystemExit as e:
        handle_system_exit(e)


def _main(
    version: Annotated[
        bool,
        Option(
            "--version",
            help="Print program version and exit.",
            show_default=False,
        ),
    ] = False
):
    """Gage ML command line interface."""
    if version:
        cli.out(f"gage {__version__}")
        raise SystemExit(0)


def handle_system_exit(e: SystemExit):
    msg, code = system_exit_params(e)
    if msg:
        cli.err(f"gage: {msg}")
    raise SystemExit(code)


def system_exit_params(e: SystemExit) -> tuple[str | None, int]:
    msg: str | None
    code: int
    if isinstance(e.code, tuple) and len(e.code) == 2:
        msg, code = cast(tuple[str, int], e.code)
    elif isinstance(e.code, int):
        msg, code = None, e.code
    else:
        msg, code = e.code, exitcodes.DEFAULT_ERROR
    return msg, code


if __name__ == "__main__":
    main()
