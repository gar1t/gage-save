# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import *

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
        help="Limit listing to [b]max[/] runs."
    )
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
    where: Where = "",
):
    """List runs."""
    from .runs_list_impl import runs_list, Args

    args = Args(
        where=where,
    )
    runs_list(args)
