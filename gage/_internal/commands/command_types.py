# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Option


RunsWhere = Annotated[
    str,
    Option(
        metavar="EXPR",
        help="Show runs matching filter expression.",
    ),
]

RunsFirst = Annotated[
    int,
    Option(
        metavar="N",
        help="Show only the first N runs.",
    ),
]
