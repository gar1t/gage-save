# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

from . import runs_support


def mark_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            runs_support.runs_arg,
            click.Option(
                ("-c", "--clear"),
                help="Clear the run's selected designation.",
                is_flag=True,
            ),
            runs_support.all_filters,
            click.Option(
                ("-y", "--yes"),
                help="Do not prompt before modifying runs.",
                is_flag=True,
            ),
        ],
    )
    return fn


@click.command("mark")
@mark_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def mark_runs(ctx: click.Context, args: Any):
    """Mark a run.

    Marked runs are used to resolve operation dependencies. If a run
    for a required operation is marked, it is used rather than the
    latest run.

    Marked runs may be viewed when listing runs using the `--marked`
    option.

    To unmark the run, use `--clear`.

    {{ runs_support.run_arg }}

    When marking, if `RUN` isn't specified, the latest unmarked run is
    used. When clearing, if `RUN` isn't specified, all marked runs
    are used.

    {{ runs_support.all_filters }}
    """
    print("TODO mark runs")

    # from . import runs_impl

    # runs_impl.mark(args, ctx)
