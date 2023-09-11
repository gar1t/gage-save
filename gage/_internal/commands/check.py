# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Option


def check(
    version: Annotated[
        str,
        Option(
            help="Test Gage version against SPEC.",
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
):
    """Show and validate Gage ML settings.

    Use `check` to show Gage ML version, install location, and other
    configured settings.
    """
    from .check_impl import check

    check(version, json)
