# SPDX-License-Identifier: Apache-2.0

from typing import *

from click import Context
from typer import Option

from .. import cli


def runs_list(
    ctx: Context,
    where: Annotated[
        str,
        Option(metavar="EXPR", help="Show runs matching filter expression."),
    ] = "",
    first: Annotated[
        int,
        Option(
            metavar="N",
            help="Show only the first N runs.",
        ),
    ] = 20,
):
    """List runs."""
    from .runs_list_impl import runs_list, Args

    args = Args(
        first=first,
    )
    cli.call_once(runs_list, [args], ctx)
