# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option


def run(
    opspec: Annotated[
        str,
        Argument(
            metavar="[OPERATION]",
            help="Operation to start.",
        ),
    ] = "",
    stage: Annotated[
        bool,
        Option(
            "--stage",
            help="Stage a run but don't run it.",
            show_default=False,
        ),
    ] = False,
    preview_sourcecode: Annotated[
        bool,
        Option(
            "--preview-sourcecode",
            help="Preview source code selection.",
            show_default=False,
        ),
    ] = False,
    preview_all: Annotated[
        bool,
        Option(
            "--preview-all",
            help="Preview all run steps without making changes.",
            show_default=False,
        ),
    ] = False,
    json: Annotated[
        bool,
        Option(
            "--json",
            help="Output preview information as JSON.",
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
            opspec=opspec,
            stage=stage,
            preview_sourcecode=preview_sourcecode,
            preview_all=preview_all,
            json=json,
        )
    )
