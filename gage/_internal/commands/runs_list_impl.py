# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

import human_readable

from .. import cli
from .. import var

from ..run_util import meta_opref
from ..run_util import run_status
from ..run_util import run_timestamp
from ..run_util import run_user_attr

__all__ = ["Args", "runs_list"]


class Args(NamedTuple):
    where: str
    first: int


def runs_list(args: Args):
    # TODO apply filter
    runs = var.list_runs(sort=["-timestamp"])
    width = cli.console_width()
    table = cli.Table(_headers(width), expand=not cli.is_plain)
    for i, run in enumerate(runs):
        table.add_row(*_row(i, run, width))
    cli.out(table)


_TRUNC_WIDTH = 60


def _headers(width: int) -> list[cli.ColSpec]:
    headers = [
        ("#", {"ratio": None, "no_wrap": True}),
        ("id", {"ratio": None, "no_wrap": True}),
        ("operation", {"ratio": None, "no_wrap": True, "max_width": 20}),
        ("started", {"ratio": None, "no_wrap": True}),
        ("status", {"ratio": None, "no_wrap": True}),
        ("label", {"ratio": 1, "no_wrap": True}),
    ]
    if width < _TRUNC_WIDTH:
        del headers[-1]
    return headers


def _row(index: int, run: Run, width: int) -> list[str]:
    opref = meta_opref(run)
    index_str = str(index)
    run_id = run.id[:8]
    op_name = opref.get_full_name()
    started = run_timestamp(run, "started")
    started_str = human_readable.date_time(started) if started else ""
    status = run_status(run)
    label = run_user_attr(run, "label") or ""

    row = [
        index_str,
        run_id,
        op_name,
        started_str,
        status,
        label,
    ]

    if width < _TRUNC_WIDTH:
        del row[-1]

    return row
