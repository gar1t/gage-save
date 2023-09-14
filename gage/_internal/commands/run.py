# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option


def run(
    operation: Annotated[
        str,
        Argument(
            metavar="[OPERATION]",
            help="Operation to start.",
        ),
    ] = "",
    preview: Annotated[
        bool,
        Option(
            "--preview",
            help="Show run steps without making any changes.",
            show_default=False,
        ),
    ] = False,
):
    """Start or stage an operation.

    **OPERATION** may be a file to run or an operation name defined in a
    project Gage file. To list available options for the current
    directory, use **gage operations**.
    """
    from .run_impl import run, Args

    run(
        Args(
            operation=operation,
            preview=preview,
        )
    )
