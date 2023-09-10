# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import click

from .. import click_util

from . import runs_support


def runs_stop_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            click.Option(
                ("-y", "--yes"), help="Do not prompt before stopping.", is_flag=True
            ),
            click.Option(
                ("--force",),
                help=(
                    "Forceably stop the runs after a period of time (specified by "
                    "'--timeout')."
                ),
                is_flag=True,
            ),
            click.Option(
                ("--timeout",),
                type=click.IntRange(min=0),
                metavar="N",
                default=30,
                help="Timeout in seconds to wait for a run to stop (default is 30).",
            ),
            runs_support.runs_arg,
            runs_support.common_filters,
        ],
    )
    return fn


@click.command(name="stop")
@runs_stop_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def stop_runs(ctx: click.Context, args: Any):
    """Stop one or more runs.

    Runs are stopped by specifying one or more RUN arguments. See SPECIFYING
    RUNS and FILTER topics for information on specifying runs to be stopped.

    Only runs with status of 'running' are considered for this operation.

    If `RUN` is not specified, the latest selected run is stopped.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``1`` is assumed (the most recent run
    with status 'running').

    {{ runs_support.common_filters }}
    """
    print("TODO")

    # from . import runs_impl

    # runs_impl.stop_runs(args, ctx)
