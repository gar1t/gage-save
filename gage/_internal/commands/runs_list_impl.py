# SPDX-License-Identifier: Apache-2.0

from typing import *

import human_readable

from .. import cli
from .. import var

from ..run_util import meta_opref
from ..run_util import run_status
from ..run_util import run_timestamp
from ..run_util import run_user_attr

__all__ = ["Args", "runs_list"]


class Args(NamedTuple):
    first: int


def runs_list(args: Args):
    runs = var.list_runs()
    table = cli.Table(
        header=[
            ("#", {"ratio": 0}),
            ("id", {"ratio": 1}),
            ("operation", {"ratio": 3}),
            ("started", {"ratio": 2, "no_wrap": True}),
            ("status", {"ratio": 2}),
            ("label", {"ratio": 4, "no_wrap": True}),
        ],
        expand=not cli.is_plain,
    )
    for index, run in enumerate(runs):
        opref = meta_opref(run)
        started = run_timestamp(run, "started")
        label = run_user_attr(run, "label")
        table.add_row(
            cli.text(str(index + 1), "yellow"),
            cli.text(run.id[:8], ""),
            cli.text(opref.get_full_name(), "bold cyan"),
            cli.text(human_readable.date_time(started), "") if started else "",
            run_status(run),
            cli.text(label, "cyan") if label else "",
        )
    cli.out(table)
