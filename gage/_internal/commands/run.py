# SPDX-License-Identifier: Apache-2.0

from typing import *

from typer import Argument
from typer import Option

OpSpec = Annotated[
    str,
    Argument(
        metavar="[operation]",
        help="Operation to start.",
    ),
]

FlagAssigns = Annotated[
    Optional[list[str]],
    Argument(
        metavar="[flag=value]...",
        help="Flag assignments.",
        show_default=False,
    ),
]

Label = Annotated[
    str,
    Option(
        "-l",
        "--label",
        metavar="label",
        help="Short label to describe the run.",
    ),
]

StageFlag = Annotated[
    bool,
    Option(
        "--stage",
        help="Stage a run but don't run it.",
        show_default=False,
    ),
]

YesFlag = Annotated[
    bool,
    Option(
        "-y",
        "--yes",
        show_default=False,
        help="Proceed without prompting.",
    ),
]

PreviewSourceCodeFlag = Annotated[
    bool,
    Option(
        "--preview-sourcecode",
        help="Preview source code selection.",
        show_default=False,
    ),
]

PreviewAllFlag = Annotated[
    bool,
    Option(
        "--preview-all",
        help="Preview all run steps without making changes.",
        show_default=False,
    ),
]

JSONFlag = Annotated[
    bool,
    Option(
        "--json",
        help="Output preview information as JSON.",
        show_default=False,
    ),
]


def run(
    opspec: OpSpec = "",
    flags: FlagAssigns = None,
    label: Label = "",
    stage: StageFlag = False,
    yes: YesFlag = False,
    preview_sourcecode: PreviewSourceCodeFlag = False,
    preview_all: PreviewAllFlag = False,
    json: JSONFlag = False,
):
    """Start or stage a run.

    [arg]operation[/] may be a file to run or an operation defined in a
    project Gage file. To list available options for the current
    directory, use '[cmd]gage operations[/]'.

    If [arg]operation[/] isn't specified, runs the default in the
    project Gage file.
    """
    from .run_impl import run, Args

    run(
        Args(
            opspec=opspec,
            flags=flags,
            label=label,
            stage=stage,
            yes=yes,
            preview_sourcecode=preview_sourcecode,
            preview_all=preview_all,
            json=json,
        )
    )
