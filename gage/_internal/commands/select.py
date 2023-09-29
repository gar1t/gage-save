# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option

__all__ = ["select"]

RunSpecs = Annotated[
    Optional[list[str]],
    Argument(
        metavar="[run]...",
        help="Runs to select.",
        show_default=False,
    ),
]

NameFlag = Annotated[
    bool,
    Option(
        "--name",
        help="Select run name.",
    ),
]


def select(runs: RunSpecs = None, name: NameFlag = False):
    """Selects runs and their attributes.

    Prints the run ID for each selected run. Selects the latest run by
    default.
    """
    from .select_impl import select, Args

    select(Args(runs, name))
