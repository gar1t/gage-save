# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option

from .. import cli

__all__ = ["check"]


def check(
    filename: Annotated[
        str,
        Argument(
            help="Check Gage file for issues. Cannot be used with --version.",
            metavar="[PATH]",
            callback=cli.excludes("version"),
        ),
    ] = "",
    version: Annotated[
        str,
        Option(
            "--version",
            help="Test Gage version against SPEC. Cannot be used with filename.",
            metavar="SPEC",
        ),
    ] = "",
    json: Annotated[
        bool,
        Option(
            "--json",
            help="Format check output as JSON.",
            show_default=False,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        Option(
            "-v",
            "--verbose",
            help="Show more information.",
            show_default=False,
        ),
    ] = False,
):
    """Show and validate settings.

    Use **check** to show Gage ML version, install location, and other
    configured settings.

    To check a Gage file for issues, specify the file as **PATH**.
    """
    from .check_impl import check, Args

    check(
        Args(
            filename=filename,
            version=version,
            json=json,
            verbose=verbose,
        )
    )
