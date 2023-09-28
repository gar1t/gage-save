# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import cli

from ..var import list_runs

from ..run_select import select_runs

from ..run_util import run_status
from ..run_util import run_timestamp
from ..run_util import run_user_attr


class Args(NamedTuple):
    run: str


def show(args: Args):
    sorted = list_runs(sort=["-timestamp"])
    selected = select_runs(sorted, [args.run or "1"])
    if not selected:
        assert False, "TODO: message can't find"
    if len(selected) > 1:
        assert False, "TODO: message too many"

    run = selected[0]

    from rich.panel import Panel
    from rich.padding import Padding
    from rich.text import Text
    from rich.console import Group

    # from rich.columns import Columns
    from rich.table import Table, Column

    status = run_status(run)
    started = run_timestamp(run, "started")
    label = run_user_attr(run, "label") or ""

    header = Table.grid(
        Column(style=cli.LABEL_STYLE),
        Column(style=cli.run_status_style(status)),
        Column(style="dim"),
        padding=1,
        collapse_padding=False,
    )
    header.add_row(
        run.opref.get_full_name(),
        status,
        _format_timestamp(started),
    )

    cli.out(
        Padding(
            Panel(
                Group(
                    *[
                        header,
                        *(
                            [
                                Padding(
                                    Text(label, style=cli.SECOND_LABEL_STYLE),
                                    (1, 0, 0, 0),
                                )
                            ]
                            if label
                            else []
                        ),
                    ]
                )
            ),
            (0, 1),
        )
    )


def _format_timestamp(ts: Any):
    if not ts:
        return ""
    import re

    s = str(ts)
    m = re.search(r"\.\d+$", s)
    if not m:
        return s
    return s[: m.start()]
