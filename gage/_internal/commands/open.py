# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option

RunSpec = Annotated[
    str,
    Argument(
        metavar="[run]",
        help=(
            "Run to show information for. Value may be an index "
            "number, run ID, or run name."
        ),
    ),
]

Path = Annotated[
    str,
    Option(
        "-p",
        "--path",
        metavar="path",
        help="Run file to open. Use '[cmd]gage show --files[/]' to show run files.",
    ),
]

Cmd = Annotated[
    str,
    Option(
        "-c",
        "--cmd",
        metavar="cmd",
        help="System command to use. Default is the system file explorer.",
    ),
]

MetaFlag = Annotated[bool, Option("-m", "--meta", hidden=True)]


def open(
    run: RunSpec = "",
    path: Path = "",
    cmd: Cmd = "",
    meta: MetaFlag = False,
):
    """Open a run in the file explorer."""

    from .open_impl import open, Args

    open(Args(run, path, cmd, meta))
