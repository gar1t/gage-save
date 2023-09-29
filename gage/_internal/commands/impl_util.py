# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import cli

from ..var import list_runs
from ..run_select import select_runs

__all__ = [
    "one_run",
]


class RunSupport(Protocol):
    @property
    def run(self) -> str:
        ...


def one_run(args: RunSupport):
    sorted = list_runs(sort=["-timestamp"])
    selected = select_runs(sorted, [args.run or "1"])
    if not selected:
        cli.err(
            f"No runs match {args.run!r}\n\n"  # \
            "Try '[b]gage list[/]' for a list of runs."
        )
        raise SystemExit()
    if len(selected) > 1:
        assert False, "TODO: message too many"

    return selected[0]
