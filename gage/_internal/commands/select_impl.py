# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import cli

from .impl_util import one_run


class Args(NamedTuple):
    runs: list[str] | None
    name: bool


class RunSupport(NamedTuple):
    run: str


def select(args: Args):
    for spec in args.runs or [""]:
        run = one_run(RunSupport(spec))
        if run:
            if args.name:
                cli.out(run.name)
            else:
                cli.out(run.id)
