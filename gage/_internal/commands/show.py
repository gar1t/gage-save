# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument

__all__ = ["show"]

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


def show(run: RunSpec = ""):
    """Show information about a run."""
    from .show_impl import show, Args

    show(Args(run))
