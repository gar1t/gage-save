# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

import human_readable

from .. import cli

from ..var import list_runs

from ..run_select import select_runs

from ..run_util import meta_opref
from ..run_util import run_status
from ..run_util import run_timestamp
from ..run_util import run_user_attr

__all__ = ["Args", "runs_list"]


class Args(NamedTuple):
    runs: list[str] | None
    more: list[bool] | None
    limit: int
    all: bool
    where: str


def runs_list(args: Args):
    sorted = list_runs(sort=["-timestamp"])
    filtered = _filter_runs(sorted, args)
    selected_with_index = _select_runs(filtered, args)
    limited_with_index = _limit_runs(selected_with_index, args)
    width = cli.console_width()
    table = cli.Table(
        *_table_cols(width),
        expand=True,
        caption=_run_table_caption(len(limited_with_index), len(filtered), args),
        caption_justify="left",
    )
    for index, run in limited_with_index:
        table.add_row(*_table_row(index, run, width))
    cli.out(table)


def _filter_runs(runs: list[Run], args: Args):
    # TODO apply where filter
    return runs


def _select_runs(runs: list[Run], args: Args):
    if not args.runs:
        return [(i + 1, run) for i, run in enumerate(runs)]
    index_lookup = {run: i + 1 for i, run in enumerate(runs)}
    selected = select_runs(runs, args.runs)
    return [(index_lookup[run], run) for run in selected]


def _run_table_caption(shown: int, filtered: int, args: Args):
    if shown == filtered:
        return None
    assert shown < filtered, (shown, filtered)
    more_help = (
        f" (use -{'m' * (len(args.more or []) + 1)} to show more)"
        if not args.runs
        else ""
    )
    return cli.pad(
        cli.text(
            f"Showing {shown} of {filtered} runs{more_help}",
            style="italic dim",
        ),
        (0, 1),
    )


def _limit_runs(runs: list[tuple[int, Run]], args: Args):
    if args.all:
        return runs
    limit = (sum(args.more or []) + 1) * args.limit
    return runs[:limit]


_TRUNC_POINTS = [
    (28, (2, 3, 4, 5)),
    (40, (3, 4, 5)),
    (60, (5,)),
]


def _table_cols(width: int) -> list[cli.ColSpec]:
    headers = [
        ("#", {"ratio": None, "no_wrap": True, "style": cli.TABLE_HEADER_STYLE}),
        ("name", {"ratio": None, "no_wrap": True, "style": "dim"}),
        ("operation", {"ratio": None, "no_wrap": True, "style": cli.LABEL_STYLE}),
        ("started", {"ratio": None, "no_wrap": True, "style": "dim"}),
        ("status", {"ratio": None, "no_wrap": True}),
        ("description", {"ratio": 1, "no_wrap": True, "style": cli.SECOND_LABEL_STYLE}),
    ]
    return _fit(headers, width)


def _table_row(index: int, run: Run, width: int) -> list[str]:
    opref = meta_opref(run)
    index_str = str(index)
    run_name = run.name[:5]
    op_name = opref.get_full_name()
    started = run_timestamp(run, "started")
    started_str = human_readable.date_time(started) if started else ""
    status = run_status(run)
    label = run_user_attr(run, "label") or ""

    row = [
        index_str,
        run_name,
        op_name,
        started_str,
        cli.text(status, style=cli.run_status_style(status)),
        label,
    ]

    return _fit(row, width)


def _fit(l: list[Any], width: int):
    for limit, drop in _TRUNC_POINTS:
        if width <= limit:
            return [x for i, x in enumerate(l) if i not in drop]
    return l
