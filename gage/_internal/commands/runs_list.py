# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import *

from .. import cli

__all__ = [
    "Where",
    "runs_list",
]

Limit = Annotated[
    int,
    Option(
        "-n",
        "--limit",
        metavar="max",
        help="Limit list to [b]max[/] runs."
    )
]

AllFlag = Annotated[
    bool,
    Option(
        "-a",
        "--all",
        help="Show all runs. Cannot use with --limit.",
        show_default=False,
        callback=cli.incompatible_with("limit"),
    ),
]

Where = Annotated[
    str,
    Option(
        metavar="expr",
        help="Show runs matching filter expression.",
    ),
]


def runs_list(
    limit: Limit = 20,
    all: AllFlag = False,
    where: Where = "",
):
    """List runs."""
    from .runs_list_impl import runs_list, Args

    args = Args(
        limit=limit,
        all=all,
        where=where,
    )
    runs_list(args)
