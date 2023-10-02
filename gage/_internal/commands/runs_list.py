# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option

from .. import cli

__all__ = [
    "Where",
    "runs_list",
]

RunArgs = Annotated[
    Optional[list[str]],
    Argument(
        metavar="[run]...",
        help=("Runs to list. [arg]run[/] may be a run ID, name, list index or slice."),
        show_default=False,
    ),
]

Limit = Annotated[
    int,
    Option(
        "-n",
        "--limit",
        metavar="max",
        help="Limit list to [b]max[/] runs.",
    ),
]

AllFlag = Annotated[
    bool,
    Option(
        "-a",
        "--all",
        help="Show all runs. Cannot use with --limit.",
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
    runs: RunArgs = None,
    limit: Limit = 20,
    all: AllFlag = False,
    where: Where = "",
):
    """List runs.

    By default the latest 20 runs are shown. To show more, use '-n /
    --limit' with higher number. Use '-a / --all' to show all runs.

    Use '-w / --where' to filter runs. Try '[cmd]gage help filters[/]'
    for help with filter expressions.

    Runs may be selected from the list using run IDs, names, indexes or
    slice notation. Try '[cmd]gage help select-runs[/]' for help with
    select options.
    """
    from .runs_list_impl import runs_list, Args

    runs_list(Args(runs, limit, all, where))
