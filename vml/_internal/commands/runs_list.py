# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

from . import remote_support
from . import runs_support


def runs_list_options(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            click.Option(
                ("-a", "--all"),
                help="Show all runs (by default only the last 20 runs are shown).",
                is_flag=True,
            ),
            click.Option(
                ("-m", "--more"),
                help=("Show 20 more runs. Maybe used multiple times."),
                count=True,
            ),
            click.Option(
                ("-n", "--limit"),
                metavar="N",
                type=click.IntRange(min=1),
                help="Limit number of runs shown.",
            ),
            click.Option(("-d", "--deleted"), help="Show deleted runs.", is_flag=True),
            runs_support.archive_option("Show archived runs in PATH."),
            click.Option(("-c", "--comments"), help="Show run comments.", is_flag=True),
            click.Option(("-v", "--verbose"), help="Show run details.", is_flag=True),
            click.Option(("--json",), help="Format runs as JSON.", is_flag=True),
            click.Option(
                ("-s", "--simplified"), help="Show a simplified list.", is_flag=True
            ),
            runs_support.all_filters,
            remote_support.remote_option("List runs on REMOTE rather than local runs."),
        ],
    )
    return fn


@click.command("list")
@runs_list_options
@click.pass_context
@click_util.use_args
@click_util.render_doc
def list_runs(ctx: click.Context, args: Any):
    """List runs.

    Run lists may be filtered using a variety of options. See below for details.

    By default, the last 20 runs are shown. Use `-a, --all` to show all runs, or
    `-m` to show more 20 more runs. You may use `-m` multiple times.

    Run indexes are included in list output for a specific listing, which is
    based on the available runs, their states, and the specified filters. You
    may use the indexes in run selection commands (e.g. ``runs delete``,
    ``compare``, etc.) but note that these indexes will change as runs are
    started, deleted, or run status changes.

    To show run detail, use `--verbose`.

    {{ runs_support.all_filters }}

    ### Show Deleted Runs

    Use `--deleted` to show deleted runs. You can use the listing for run IDs
    and indexes to use in ``runs restore`` (restore runs) and ``runs purge``
    (permanently delete runs).

    {{ runs_support.archive_option }}

    ### Show Remote Runs

    To list runs on a remote, specify `--remote REMOTE`. Use ``guild remotes``
    to list available remotes.

    For information on configuring remotes, see ``guild remotes --help``.
    """
    print("TODO: list runs")

    # from . import runs_impl

    # runs_impl.list_runs(args, ctx)
