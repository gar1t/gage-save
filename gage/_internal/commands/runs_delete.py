# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import *

__all__ = ["runs_delete"]

Runs = Annotated[
    Optional[list[str]],
    Argument(
        help="Runs to delete.",
        metavar="[run]...",
        show_default=False,
    ),
]

Where = Annotated[
    str,
    Option(
        metavar="expr",
        help="Delete runs matching filter expression.",
    ),
]


def runs_delete(runs: Runs = None, where: Where = ""):
    """Delete runs.

    [arg]run[/] is either a run index, a run ID, or a run name. Partial
    values may be specified for run ID and run name if they uniquely
    identify a run. Multiple runs may be specified.
    """
    from .runs_delete_impl import runs_delete, Args

    runs_delete(Args(runs, where))
