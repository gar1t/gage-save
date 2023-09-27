# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import *

__all__ = [
    "Where",
    "runs_list",
]

Where = Annotated[
    str,
    Option(
        metavar="EXPR",
        help="Show runs matching filter expression.",
    ),
]


def runs_list(
    where: Where = "",
):
    """List runs."""
    from .runs_list_impl import runs_list, Args

    args = Args(
        where=where,
    )
    runs_list(args)
