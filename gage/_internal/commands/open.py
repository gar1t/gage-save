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


def open(run: RunSpec = "", cmd: Cmd = "", meta: MetaFlag = False):
    """Open a run in the file explorer."""

    from .open_impl import open, Args

    open(Args(run, cmd, meta))
