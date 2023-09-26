# SPDX-License-Identifier: Apache-2.0

from typing import *

import human_readable

from .. import cli
from .. import var

from ..run_util import meta_opref
from ..run_util import run_status
from ..run_util import run_timestamp

__all__ = ["Args", "runs_list"]


class Args(NamedTuple):
    first: int


def runs_list(args: Args):
    runs = var.list_runs()
    table = cli.Table(header=["#", "id", "operation", "started", "status"])
    for index, run in enumerate(runs):
        opref = meta_opref(run)
        started = run_timestamp(run, "started")
        table.add_row(
            cli.text(str(index + 1), "dim"),
            run.id[:8],
            cli.text(opref.get_full_name(), "bold cyan"),
            human_readable.date_time(started) if started else "",
            run_status(run),
        )
    cli.out(table)
